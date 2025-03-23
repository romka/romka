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

TELEGRAM_CONTENT_TYPES = os.environ.get("TELEGRAM_CONTENT_TYPES", "content/blog,content/note").split(",")
MAPPINGS_PATH = Path("telegram-data/telegram_mappings.csv")

# DON'T CHANGE ANYTHING BELOW THIS LINE
# Utils
TYPE_TEXT = "text"
TYPE_MEDIA = "media"
TYPE_PHOTO = "photo"


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
    return any(str(path).startswith(t.strip() + "/") for t in TELEGRAM_CONTENT_TYPES)


def sanitize_telegram_html(html: str) -> str:
    html = re.sub(r"</p\s*>", "\n", html)
    html = re.sub(r"<p\s*>", "", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = re.sub(r"<hr\s*/?>", "\n\n", html)
    return html.strip()


def cleanup_raw_text(text: str) -> str:
    # Remove Hugo shortcodes like {{< ... >}}
    text = re.sub(r"\{\{<[^>]+>\}\}", "", text)

    # Replace inline code with <code> tags
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Remove unsupported HTML tags like <img>, <div>, <iframe>, etc.
    text = re.sub(r"<img\s+[^>]*>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<div\s+[^>]*>|</div>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"<iframe\s+[^>]*>|</iframe>", "", text, flags=re.IGNORECASE)

    return text


def build_message(post, url: str, lang: str) -> str:
    title_raw = post.get("title", "")
    content_parts = post.content.split("<!--more-->")
    preview_raw = content_parts[0].strip()
    has_more = len(content_parts) > 1 and content_parts[1].strip()

    read_more_text = LANG_TO_TELEGRAM[lang]["read_more_text"]

    preview_raw = cleanup_raw_text(preview_raw)

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

        if not post.content:
            print(f"⚠️  Empty content in {rel_path}, skipping")
            continue

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
                    type = TYPE_PHOTO  # it's not a mistake, it's also a single photo
                    # Send first photo with the text
                    message_id = send_photo_with_caption(config["token"], config["chat_id"], image_paths[0], message)
                    print("🖼️ Sent post with first image and caption")

                    # Send the remaining images as a separate mediaGroup. MediaGroups are not editable in Telegram,
                    # that's why sending is split: to keep opportunity to edit the text
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
