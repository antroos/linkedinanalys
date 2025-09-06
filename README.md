## 🤖 Telegram OCR Bot (OpenAI GPT-4o Vision)

A Telegram bot that extracts text from images using OpenAI GPT-4o Vision and stores results in SQLite.

### 🚀 Features

- 📷 Extracts text and numbers from images (JPG, PNG, GIF, WebP)
- 🧠 Uses OpenAI GPT-4o Vision for high-precision OCR
- 💾 Persists results to SQLite with file name and timestamp
- 📤 Commands to preview recent results and export CSV

### ⚙️ Setup

1) Install dependencies
```bash
pip install -r requirements.txt
```

2) Provide environment variables
```bash
export TELEGRAM_TOKEN="<your_telegram_bot_token>"
export OPENAI_API_KEY="<your_openai_api_key>"
```

3) Run the bot
```bash
python main.py
```

### 📱 Usage

1. Find your bot in Telegram
2. Send `/start`
3. Send an image with text
4. Receive extracted text

Bot commands:
- `/start` — show welcome
- `/help` — usage guide
- `/status` — bot status
- `/results` — last 5 parsed records from DB
- `/export` — export all results to CSV

### 🛠 Tech details

- `python-telegram-bot` for Telegram API
- `requests` for OpenAI HTTP calls
- `Pillow` for image handling (if needed)
- `sqlite3` for storage

### 🧱 Architecture

- Async handlers (`python-telegram-bot` v20)
- Download image from Telegram → base64 → OpenAI Vision → text
- Save to `image_analysis_results.db` → table `file_parse_results`

### 💰 Costs

OpenAI API usage is paid. Check current pricing at `https://openai.com/pricing`.

### 🧪 Local development

Project layout:
```
LIanalys/
├── main.py              # Telegram bot
├── create_analysis_database.py  # Sample DB generator
├── view_database.py     # DB viewer (CLI)
├── requirements.txt     # Dependencies
└── README.md            # This file
```

Logs are written to `bot.log`.

### 📄 License

Educational use. Follow Telegram and OpenAI usage policies.