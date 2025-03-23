Contents of Roman Arkharov’s personal blog [romka.eu](https://romka.eu).

Mirrors of the blog are available on [Render](https://romka-eu.onrender.com/), [Netlify](https://nimble-figolla-e0e98e.netlify.app/), and IPFS.

---

### 📬 Telegram Integration for Hugo Blog

This project includes a helper script for automatically sending selected blog posts to a Telegram channel.

#### 🎯 Purpose

The setup is designed to automate Telegram publishing for a multilingual Hugo blog, using frontmatter metadata like `telegram: true`. It supports Telegram’s Markdown formatting and tracks which posts have already been sent or updated.

You don't need to worry about the Python internals — `venv` and `requirements.txt` are simply support tools that make the Telegram integration work smoothly.

#### 📁 Project Structure
```
.
├── content/
├── telegram-data/
│   └── post_to_telegram.py
│   └── telegram_mappings.csv
├── requirements.txt
└── venv/ (optional, local)
```

- `telegram-data/post_to_telegram.py` — the main script that reads your Hugo Markdown posts and sends them to Telegram via the Bot API.
- `telegram-data/telegram_mappings.csv` — a CSV file that maps each blog post’s relative path and language to its corresponding Telegram `message_id`, along with timestamps of when it was first sent or last updated.

#### ⚙️ Configuration

Before running the script, make sure to configure the following:

- `BASE_URL` — the public URL of your blog, set at the top of `post_to_telegram.py` (e.g., `https://myblog.com`).
- Telegram bot credentials per language:
    - `TELEGRAM_BOT_TOKEN_<LANG>` — the bot token for the target language (e.g., `TELEGRAM_BOT_TOKEN_RU`)
    - `TELEGRAM_CHAT_ID_<LANG>` — the channel or group ID for the corresponding language (e.g., `TELEGRAM_CHAT_ID_RU`)
- *(Optional)* `TELEGRAM_CONTENT_TYPES` — a comma-separated list of content folders to scan (e.g., `content/blog,content/note`)

All configuration values should be set via environment variables before running the script.

#### 🤖 Automating with GitHub Actions

The `telegram-data/post_to_telegram.py` script is GitHub Actions–friendly. You can set up a workflow to trigger on every push to the `main` branch, detect which Markdown files were changed, and pass those files to the script.

Thanks to GitHub’s built-in secret management, Telegram bot tokens and channel IDs can be stored securely and injected at runtime. This makes the publishing process fully automated and seamlessly integrated into your content workflow.
