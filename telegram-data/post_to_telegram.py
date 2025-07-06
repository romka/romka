#!/usr/bin/env python3
"""
### Telegram Post Publisher for Static Blog

This script is designed to automatically send blog posts from a Hugo-based static site to a Telegram channel.
It can be run manually or triggered automatically via GitHub Actions on every push to the `main` branch.

Each post is a Markdown file with [YAML frontmatter](https://jekyllrb.com/docs/front-matter/). Posts marked with
`telegram: true` will be published to the configured Telegram channel.

#### Features

- Converts Markdown to Telegram HTML format
- Supports three post types:
  - Plain text
  - A single image with caption
  - A captioned image followed by a gallery
- Detects and escapes necessary HTML characters
  - Adds "read more" link if the `<!--more-->` tag is used
  - Supports `<spoiler>` tags for hidden text in Telegram
  - Tracks sent messages in `telegram_mappings.csv` and updates them if modified

---

### Setup

#### Required environment variables (per language):

Each language used in posts must have corresponding bot token and chat ID environment variables set:

```bash
TELEGRAM_BOT_TOKEN_RU=your_bot_token
TELEGRAM_CHAT_ID_RU=@your_channel_username
```

Add more languages by expanding the LANG_TO_TELEGRAM dictionary in the script.

#### Post configuration

To send a post, include the following in its frontmatter:

- `telegram: true`
- `telegram_images: image1.jpg, image2.jpg`  # optional

The images must be located in the same folder as the Markdown file. **Files over 10 MB will be skipped** with a warning.
Automation

A GitHub Actions workflow can be used to automatically run this script when new posts are pushed to the repository.
The workflow should:
- Set up Python and dependencies (frontmatter, markdown, etc.)
- Provide the necessary environment variables
- Run post_to_telegram.py with changed Markdown files as arguments

See the accompanying GitHub Action .yml file for an example.

#### Editing Messages

After a post is published:
- Text-only and single-image posts can be edited using Telegram Bot API.
- Multi-image posts consist of two messages: only the one with the first image and caption is editable.

All sent messages are tracked in `telegram_mappings.csv`, which is automatically updated by the script.
"""
import os
import csv
import json
import sys
import re
import frontmatter
import requests
import markdown
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict

# Configuration
BASE_URL = "https://romka.eu"
DEFAULT_LANGUAGE = "ru"
LANG_TO_TELEGRAM = {
    "ru": {
        "token_env": "TELEGRAM_BOT_TOKEN_RU",
        "chat_id_env": "TELEGRAM_CHAT_ID_RU",
        "read_more_text": "Читать весь текст в блоге"
    },
    # "en": {
    #     "token_env": "TELEGRAM_BOT_TOKEN_EN",
    #     "chat_id_env": "TELEGRAM_CHAT_ID_EN",
    #     "read_more_text": "Read the full post on the blog"
    # }
}

TELEGRAM_TEXT_CONTENT_TYPES = os.environ.get("TELEGRAM_CONTENT_TYPES", "content/blog,content/note").split(",")
TELEGRAM_PHOTO_CONTENT_PATHS = ("content/gallery", "content/story")
MAPPINGS_PATH = Path("telegram-data/telegram_mappings.csv")
MAX_SIZE = 49 * 1024 * 1024
MAX_FILE_SIZE = 9.5 * 1024 * 1024

# DON'T CHANGE ANYTHING BELOW THIS LINE
# Utils
TYPE_TEXT = "text"
TYPE_MEDIA = "media"
TYPE_PHOTO = "photo"
TYPE_IMAGE_ONLY = "image_only"


def escape_html(text: str) -> str:
    """Escape only necessary HTML characters for Telegram HTML mode."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def detect_lang_from_filename(filename: str) -> str | None:
    match = re.search(r"\.([a-z]{2})\.md$", filename)
    if match:
        lang = match.group(1)
        if lang in LANG_TO_TELEGRAM:
            return lang
    return None


def get_telegram_config(lang: str) -> dict:
    config = LANG_TO_TELEGRAM.get(lang)
    if not config:
        raise ValueError(f"Unsupported language: {lang}")
    token = os.environ.get(config["token_env"])
    chat_id = os.environ.get(config["chat_id_env"])
    if not token or not chat_id:
        raise EnvironmentError(f"Missing TELEGRAM config for language '{lang}'")
    return {
        "token": token,
        "chat_id": chat_id,
        "read_more_text": config["read_more_text"]
    }


def read_mappings() -> dict:
    mappings = {}
    if MAPPINGS_PATH.exists():
        with MAPPINGS_PATH.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row: Dict[str, str]
                key = (row["relative_path"], row["lang"])
                mappings[key] = {
                    "message_id": int(row["message_id"]),
                    "published_to_telegram_at": row["published_to_telegram_at"],
                    "updated_at": row["updated_at"] or "",
                    "type": row.get("type", "text")
                }
    return mappings


def write_mappings(mappings: dict):
    with MAPPINGS_PATH.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["message_id", "relative_path", "lang", "type", "published_to_telegram_at", "updated_at"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for (rel_path, lang), meta in sorted(mappings.items()):
            writer.writerow({
                "message_id": meta["message_id"],
                "relative_path": rel_path,
                "lang": lang,
                "type": meta.get("type", "text"),
                "published_to_telegram_at": meta["published_to_telegram_at"],
                "updated_at": meta.get("updated_at", "")
            })


def is_allowed_path(path: Path) -> bool:
    return any(str(path).startswith(t.strip() + "/") for t in TELEGRAM_TEXT_CONTENT_TYPES + list(TELEGRAM_PHOTO_CONTENT_PATHS))


def sanitize_telegram_html(html: str) -> str:
    # Remove unsupported tags completely
    html = re.sub(r"<img\b[^>]*\/?>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?div\b[^>]*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"</?iframe\b[^>]*>", "", html, flags=re.IGNORECASE)

    # Format paragraphs and line breaks for Telegram
    html = re.sub(r"</p\s*>", "\n", html)
    html = re.sub(r"<p\s*>", "", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"<hr\s*/?>", "\n\n", html)
    html = re.sub(r"<spoiler>", "<tg-spoiler>", html)
    html = re.sub(r"</spoiler>", "</tg-spoiler>", html)

    html = html.replace("---", "—")
    html = html.replace("&mdash;", "—")
    html = html.replace("&ndash;", "—")
    html = html.replace("--", "—")

    return html.strip()


def cleanup_raw_text(text: str) -> str:
    # Remove Hugo shortcodes like {{< ... >}}
    text = re.sub(r"\{\{<[^>]+>\}\}", "", text)

    # Replace inline code with <code> tags
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    return text


def stylize_bullet_lines(text: str) -> str:
    lines = text.splitlines()
    output = []
    in_bullet_block = False

    for line in lines:
        if line.strip().startswith("- "):
            if not in_bullet_block:
                output.append("")  # blank line before the block
                in_bullet_block = True
            output.append("  • " + line.strip()[2:].strip())
        else:
            if in_bullet_block:
                output.append("")  # blank line after the block
                in_bullet_block = False
            output.append(line)
    if in_bullet_block:
        output.append("")
    return "\n".join(output)


def build_message(post, url: str, lang: str) -> str:
    title_raw = post.get("title", "")
    content_parts = post.content.split("<!--more-->")
    preview_raw = content_parts[0].strip()
    has_more = len(content_parts) > 1 and content_parts[1].strip()

    read_more_text = LANG_TO_TELEGRAM[lang]["read_more_text"]

    preview_raw = stylize_bullet_lines(cleanup_raw_text(preview_raw))

    parts = []

    if title_raw:
        parts.append(f"<b>{escape_html(title_raw)}</b>")

    content_html = markdown.markdown(preview_raw)
    content_html = sanitize_telegram_html(content_html)
    parts.append(content_html)

    if has_more:
        read_more_link = f'<a href="{escape_html(url)}">{escape_html(read_more_text)}</a>'
        parts.append(read_more_link)

    return "\n\n".join(parts)


def extract_image_list_from_gallery(post, path: Path) -> list[list[str]]:
    """
    Extract images from gallery and split them into multiple galleries if total size exceeds MAX_SIZE.
    Returns a list of lists, where each inner list represents a gallery with images that fit within MAX_FILE_SIZE.
    """
    if not post.content.strip():
        base_path = path.parent
        galleries = []
        current_gallery = []
        current_size = 0
        image_limit = 10
        print(f"ℹ️ Post content empty for {path}. Scanning directory {base_path} for images.")
        try:
            # Find potential image files first
            potential_files = sorted([
                f for f in base_path.iterdir()
                if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png"]
            ])

            # Iterate and check size/count limits
            for f in potential_files:
                try:
                    file_size = f.stat().st_size
                    
                    # If adding this file would exceed MAX_SIZE, start a new gallery
                    if current_size + file_size > MAX_SIZE:
                        if current_gallery:  # Only add non-empty galleries
                            galleries.append(current_gallery)
                            print(f"ℹ️ Created a gallery with {len(current_gallery)} images, total size: {current_size} bytes.")
                            current_gallery = []
                            current_size = 0
                    
                    # Add file to current gallery if it fits
                    if file_size <= MAX_FILE_SIZE:  # Skip files larger than MAX_FILE_SIZE entirely
                        current_gallery.append(f.name)
                        current_size += file_size
                        
                        # If we've reached the image limit for this gallery, start a new one
                        if len(current_gallery) >= image_limit:
                            galleries.append(current_gallery)
                            print(f"ℹ️ Reached image limit ({image_limit}) for gallery. Created a gallery with {len(current_gallery)} images, total size: {current_size} bytes.")
                            current_gallery = []
                            current_size = 0
                    else:
                        print(f"⚠️ File {f.name} ({file_size} bytes) exceeds maximum size limit and will be skipped.")
                        
                except FileNotFoundError:
                    print(f"⚠️ File not found during size check: {f}")
                    continue
                except Exception as e:
                    print(f"❌ Error getting size for file {f}: {e}")
                    continue  # Skip file if size check fails

            # Add the last gallery if it's not empty
            if current_gallery:
                galleries.append(current_gallery)
                print(f"ℹ️ Created a final gallery with {len(current_gallery)} images, total size: {current_size} bytes.")

            total_images = sum(len(gallery) for gallery in galleries)
            print(f"ℹ️ Selected {total_images} images across {len(galleries)} galleries from directory scan.")
            return galleries if galleries else [[]]  # Return at least one empty gallery if none were created

        except FileNotFoundError:
            print(f"❌ Directory not found: {base_path}")
            return [[]]
        except Exception as e:
            print(f"❌ Error listing or processing files in {base_path}: {e}")
            return [[]]

    # Process content from post
    all_images = []
    for line in post.content.strip().splitlines():
        parts = line.strip().split(";")
        if parts and parts[0]:
            all_images.append(parts[0].strip())
    
    # Split images into galleries of max 10 images each
    galleries = []
    current_gallery = []
    current_size = 0
    
    for img_name in all_images:
        img_path = path.parent / img_name
        try:
            if not img_path.exists():
                print(f"⚠️ Image file not found: {img_path}")
                continue
                
            file_size = img_path.stat().st_size
            
            # If adding this file would exceed MAX_SIZE, start a new gallery
            if current_size + file_size > MAX_SIZE and current_gallery:
                galleries.append(current_gallery)
                current_gallery = []
                current_size = 0
            
            # Add file to current gallery if it fits
            if file_size <= MAX_SIZE:  # Skip files larger than MAX_SIZE entirely
                current_gallery.append(img_name)
                current_size += file_size
                
                # If we've reached the image limit for this gallery, start a new one
                if len(current_gallery) >= 10:  # Telegram limit is 10 images per media group
                    galleries.append(current_gallery)
                    current_gallery = []
                    current_size = 0
            else:
                print(f"⚠️ File {img_name} ({file_size} bytes) exceeds maximum size limit and will be skipped.")
                
        except Exception as e:
            print(f"❌ Error processing image {img_name}: {e}")
            continue
    
    # Add the last gallery if it's not empty
    if current_gallery:
        galleries.append(current_gallery)
    
    total_images = sum(len(gallery) for gallery in galleries)
    print(f"ℹ️ Selected {total_images} images across {len(galleries)} galleries from post content.")
    return galleries if galleries else [[]]  # Return at least one empty gallery if none were created


def send_photo_with_caption(token: str, chat_id: str, image_path: Path, caption: str) -> int:
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    with open(image_path, "rb") as photo_file:
        files = {
            "photo": photo_file
        }
        data = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        response = requests.post(url, data=data, files=files)

    if not response.ok:
        print("📭 Telegram API error (photo with caption):")
        print(response.text)
        response.raise_for_status()

    return response.json()["result"]["message_id"]


def send_media_with_caption(token: str, chat_id: str, image_paths: list[Path], caption: str) -> int:
    """Send a media group with caption. Returns the message ID of the first message in the group."""
    url = f"https://api.telegram.org/bot{token}/sendMediaGroup"
    media = []
    files = {}

    for i, path in enumerate(image_paths):
        field = f"photo{i}"
        files[field] = open(path, "rb")
        item = {
            "type": "photo",
            "media": f"attach://{field}"
        }
        if i == 0:
            item["caption"] = caption
            item["parse_mode"] = "HTML"
        media.append(item)

    data = {
        "chat_id": chat_id,
        "media": json.dumps(media)
    }

    response = requests.post(url, data=data, files=files)
    for f in files.values():
        f.close()

    if not response.ok:
        print("📭 Telegram API error (media with caption):")
        print(response.text)
        response.raise_for_status()

    result = response.json()["result"]
    return result[0]["message_id"]


def send_additional_images(token: str, chat_id: str, image_paths: list[Path]):
    if not image_paths:
        return

    url = f"https://api.telegram.org/bot{token}/sendMediaGroup"
    media = []
    files = {}

    for i, path in enumerate(image_paths):
        field = f"photo{i}"
        files[field] = open(path, "rb")
        media.append({
            "type": "photo",
            "media": f"attach://{field}"
        })

    data = {
        "chat_id": chat_id,
        "media": json.dumps(media)
    }

    response = requests.post(url, data=data, files=files)
    for f in files.values():
        f.close()

    if not response.ok:
        print("📭 Telegram API error (additional images):")
        print(response.text)
        response.raise_for_status()


def send_to_telegram(token: str, chat_id: str, text: str) -> int:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=payload)

    if not response.ok:
        print("📭 Telegram API error response:")
        print(response.text)

    response.raise_for_status()
    return response.json()["result"]["message_id"]


def edit_telegram_message(token: str, chat_id: str, message_id: int, text: str, type: str):
    if type == TYPE_TEXT:
        url = f"https://api.telegram.org/bot{token}/editMessageText"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
    elif type == TYPE_PHOTO:
        url = f"https://api.telegram.org/bot{token}/editMessageCaption"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": text,
            "parse_mode": "HTML"
        }
    elif type == TYPE_MEDIA:
        print("⚠️ Cannot edit media group messages")
        return
    else:
        print(f"⚠️ Unknown message type '{type}', skipping edit")
        return

    response = requests.post(url, data=payload)

    if not response.ok:
        print("📭 Telegram API error response:")
        print(response.text)

    response.raise_for_status()


# Main logic


def main():
    if len(sys.argv) < 2:
        print("Usage: post_to_telegram.py path1.md [path2.md ...]")
        return

    mappings = read_mappings()
    updated = False
    now = datetime.now(timezone.utc).isoformat()

    for path_str in sys.argv[1:]:
        path = Path(path_str)
        rel_path = str(path)

        if not path.exists() or path.suffix != ".md":
            print("ℹ️ Path " + str(path) + " does not exist, or doesn't contain md file")
            continue
        if not is_allowed_path(path):
            continue

        lang = detect_lang_from_filename(rel_path)
        if not lang:
            continue

        config = get_telegram_config(lang)
        post = frontmatter.load(str(path))

        if not post.get("telegram", False):
            continue

        relative_parts = path.relative_to("content").parts[:-1]
        url_path = "/".join(relative_parts)
        if lang != DEFAULT_LANGUAGE:
            url_path = f"{lang}/{url_path}"
        url = f"{BASE_URL}/{url_path}/"

        is_photo_content = any(str(path).startswith(p) for p in TELEGRAM_PHOTO_CONTENT_PATHS)
        has_telegram_images = post.get("telegram_images")

        if not post.content and not is_photo_content and not has_telegram_images:
            print(f"⚠️  Empty content in {rel_path}, skipping")
            continue

        # --- Process galleries and stories ---
        if is_photo_content:
            gallery_groups = extract_image_list_from_gallery(post, path)
            first_message_id = None
            
            for gallery_index, gallery in enumerate(gallery_groups):
                image_paths = []
                for fname in gallery:
                    full_path = path.parent / fname
                    if not full_path.exists():
                        print(f"⚠️ Image file not found: {full_path}")
                        continue
                    if full_path.stat().st_size > 10 * 1024 * 1024:
                        print(f"⚠️ Image file too large (>10MB), skipping: {full_path.name}")
                        continue
                    image_paths.append(full_path)

                if not image_paths:
                    print(f"⚠️ No valid images in gallery group {gallery_index+1}: {rel_path}")
                    continue

                # Only add caption to the first gallery
                caption = ""
                if gallery_index == 0:
                    caption = f"<b>{escape_html(str(post.get('title', '')))}</b>"
                    total_images = sum(len(g) for g in gallery_groups)
                    if total_images > 10 or len(gallery_groups) > 1:
                        caption += f"\n\n<a href=\"{escape_html(url)}\">Читать полностью</a>"
                
                try:
                    message_id = send_media_with_caption(config["token"], config["chat_id"], image_paths, caption)
                    
                    # Store the first message ID for mapping
                    if gallery_index == 0:
                        first_message_id = message_id
                        mappings[(rel_path, lang)] = {
                            "message_id": message_id,
                            "published_to_telegram_at": now,
                            "updated_at": "",
                            "type": TYPE_MEDIA
                        }
                    
                    print(f"📸 Sent image gallery {gallery_index+1}/{len(gallery_groups)}: {rel_path} with {len(image_paths)} images")
                except Exception as e:
                    print(f"❌ Failed to send gallery {gallery_index+1}/{len(gallery_groups)}: {e}")
            
            if first_message_id:
                updated = True
                print(f"📸 Completed sending all galleries for: {rel_path}")
            else:
                print(f"⚠️ Failed to send any galleries for: {rel_path}")
            
            continue

        # --- Process blog/note (text content) ---
        message = build_message(post, url, lang)
        key = (rel_path, lang)

        if key in mappings:
            try:
                print("DEBUG message:")
                print(message)
                edit_telegram_message(config["token"], config["chat_id"], mappings[key]["message_id"], message,
                                      mappings[key]["type"])
                mappings[key]["updated_at"] = now
                print(f"🔁 Updated Telegram message for {rel_path}")
                updated = True
            except Exception as e:
                print(f"❌ Failed to update message {rel_path}: {e}")
        else:
            try:
                print("DEBUG message:")
                print(message)

                telegram_images = post.get("telegram_images")
                image_paths = []

                if telegram_images:
                    image_filenames = [img.strip() for img in str(telegram_images).split(",")]
                    for fname in image_filenames:
                        full_path = path.parent / fname
                        if not full_path.exists():
                            print(f"⚠️  Image file not found: {full_path}")
                            continue
                        if full_path.stat().st_size > 10 * 1024 * 1024:
                            print(f"⚠️  Image file too large (>10MB), skipping: {full_path.name}")
                            continue
                        image_paths.append(full_path)

                if not image_paths:
                    type = TYPE_TEXT
                    message_id = send_to_telegram(config["token"], config["chat_id"], message)
                    print("📤 Sent post without images")

                elif len(image_paths) == 1:
                    type = TYPE_PHOTO
                    message_id = send_photo_with_caption(config["token"], config["chat_id"], image_paths[0], message)
                    print("🖼️ Sent post with one image and caption")

                else:
                    type = TYPE_PHOTO
                    message_id = send_photo_with_caption(config["token"], config["chat_id"], image_paths[0], message)
                    print("🖼️ Sent post with first image and caption")
                    try:
                        send_additional_images(config["token"], config["chat_id"], image_paths[1:])
                        print(f"🖼️ Sent additional {len(image_paths) - 1} image(s)")
                    except Exception as e:
                        print(f"⚠️ Failed to send additional images: {e}")

                mappings[key] = {
                    "message_id": message_id,
                    "published_to_telegram_at": now,
                    "updated_at": "",
                    "type": type
                }

                if type == TYPE_PHOTO and len(image_paths) > 1:
                    extra_key = (rel_path + "#media", lang)
                    mappings[extra_key] = {
                        "message_id": -message_id,
                        "published_to_telegram_at": now,
                        "updated_at": "",
                        "type": TYPE_MEDIA
                    }

                updated = True
                print(f"📤 Sent new post: {rel_path} → message_id={message_id}")
            except Exception as e:
                print(f"❌ Failed to send new post {rel_path}: {e}")

    if updated:
        write_mappings(mappings)
        print("✅ Mapping file updated.")
    else:
        print("ℹ️ No new messages sent.")


if __name__ == "__main__":
    main()
