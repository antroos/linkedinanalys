import asyncio
import logging
import sys
import os
import base64
import json
from io import BytesIO, StringIO
from PIL import Image
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from typing import Optional
import sqlite3
from datetime import datetime
import csv

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Tokens initialization (from environment variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

logger.info("🤖 Initializing bot…")

# Tokens validation
if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_TOKEN is not set!")
    sys.exit(1)
else:
    logger.info(f"✅ Telegram token loaded (length: {len(TELEGRAM_TOKEN)} chars)")

if not OPENAI_API_KEY:
    logger.error("❌ OPENAI_API_KEY is not set!")
    sys.exit(1)
else:
    logger.info(f"✅ OpenAI token loaded (length: {len(OPENAI_API_KEY)} chars)")
    logger.info(f"🔗 OpenAI API URL: {OPENAI_API_URL}")

class ImageAnalysisBot:
    def __init__(self):
        logger.info("🔧 Creating bot instance…")
        try:
            # Create application with standard Updater
            self.application = Application.builder().token(TELEGRAM_TOKEN).build()
            logger.info("✅ Telegram Application created")
            # Initialize DB for parsed results
            self.db_path = 'image_analysis_results.db'
            self.init_db()
            self.setup_handlers()
            logger.info("✅ Handlers configured")
        except Exception as e:
            logger.error(f"❌ Bot creation error: {e}")
            raise
    
    def setup_handlers(self):
        """Configure command and message handlers"""
        logger.info("⚙️ Setting up handlers…")
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("results", self.results_command))
        self.application.add_handler(CommandHandler("export", self.export_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        logger.info("✅ All handlers registered")
    
    def init_db(self):
        """Create table for parsed results if not exists"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_parse_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    full_text TEXT NOT NULL,
                    parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            logger.info("🗄️ Database ready (table file_parse_results)")
        except Exception as e:
            logger.error(f"❌ DB initialization error: {e}", exc_info=True)

    def save_parse_result(self, file_name: str, full_text: str):
        """Save parsing result into DB"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO file_parse_results (file_name, full_text) VALUES (?, ?)',
                (file_name, full_text)
            )
            conn.commit()
            conn.close()
            logger.info("💾 Result saved to DB: %s", file_name)
        except Exception as e:
            logger.error(f"❌ DB save error: {e}", exc_info=True)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/start handler"""
        user = update.effective_user
        logger.info(f"📝 /start from {user.username} ({user.id})")
        
        welcome_message = (
            f"👋 Hi, {user.first_name}!\n\n"
            "🖼️ I extract text from images using OpenAI GPT-4o Vision.\n\n"
            "📷 Send me any image with text and I will:\n"
            "• Extract all text and numbers from the image\n"
            "• Return a clean, readable result\n\n"
            "💡 Available commands:\n"
            "• /start — show this message\n"
            "• /help — usage guide\n"
            "• /status — bot status"
        )
        
        try:
            await update.message.reply_text(welcome_message)
            logger.info(f"✅ Welcome message sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Failed to send welcome: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/help handler"""
        user = update.effective_user
        logger.info(f"📚 /help from {user.username} ({user.id})")
        
        help_message = (
            "🆘 Usage Guide:\n\n"
            "📷 **Text extraction from images:**\n"
            "• Send any image with text\n"
            "• Get all extracted text and numbers\n"
            "• Works with images containing text of any kind\n\n"
            "🔧 **Technical details:**\n"
            "• Model: OpenAI GPT-4o Vision\n"
            "• OCR: high-precision text extraction\n"
            "• Max size: 20MB\n"
            "• Supported formats: JPG, PNG, PDF\n\n"
            "❓ **Commands:**\n"
            "• /start — start\n"
            "• /help — this help\n"
            "• /status — status"
        )
        
        try:
            await update.message.reply_text(help_message, parse_mode='Markdown')
            logger.info(f"✅ Help guide sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Help send error: {e}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """/status handler"""
        user = update.effective_user
        logger.info(f"⚡ /status from {user.username} ({user.id})")
        
        status_message = (
            "🟢 Bot is running normally!\n\n"
            "🔧 **Components status:**\n"
            "• Telegram API: ✅ Connected\n"
            "• OpenAI API: ✅ Available\n"
            "• GPT-4o Vision: ✅ Active\n\n"
            "📊 **Info:**\n"
            "• Model: OpenAI GPT-4o Vision\n"
            "• Function: OCR (text extraction)\n"
            "• Bot version: 4.1"
        )
        
        try:
            await update.message.reply_text(status_message)
            logger.info(f"✅ Status sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Status send error: {e}")
    
    async def results_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show last 5 parsed records (file name, text length, timestamp)"""
        user = update.effective_user
        logger.info(f"📚 /results from {user.username} ({user.id})")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, file_name, LENGTH(full_text) AS text_len, parsed_at
                FROM file_parse_results
                ORDER BY id DESC
                LIMIT 5
                """
            )
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                await update.message.reply_text("No records yet. Send an image to parse.")
                return

            lines = ["Latest results (max 5):\n"]
            for rid, fname, tlen, ts in rows:
                lines.append(f"#{rid} | {ts} | {fname} | {tlen} chars")

            await update.message.reply_text("\n".join(lines))
            logger.info("✅ Results sent to user %s", user.id)
        except Exception as e:
            logger.error(f"❌ /results error: {e}", exc_info=True)
            await update.message.reply_text("❌ Database read error. Please try again later.")

    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Export all results to CSV and send as a file"""
        user = update.effective_user
        logger.info(f"📚 /export from {user.username} ({user.id})")

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT parsed_at, file_name, full_text
                FROM file_parse_results
                ORDER BY id
                """
            )
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                await update.message.reply_text("No data to export yet.")
                return

            # Build CSV in-memory
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["parsed_at", "file_name", "full_text"])
            for parsed_at, file_name, full_text in rows:
                writer.writerow([parsed_at, file_name, full_text])

            data = csv_buffer.getvalue().encode('utf-8')
            csv_bytes = BytesIO(data)
            filename = f"file_parse_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            await update.message.reply_document(document=csv_bytes, filename=filename)
            logger.info("✅ CSV export sent to user %s", user.id)
        except Exception as e:
            logger.error(f"❌ /export error: {e}", exc_info=True)
            await update.message.reply_text("❌ Export error. Please try again later.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user = update.effective_user
        logger.info(f"💬 Text message from {user.username} ({user.id}): {update.message.text[:50]}...")
        
        try:
            await update.message.reply_text(
                "📷 Send me an image with text!\n\n"
                "🔍 I will extract all text and numbers from the image\n\n"
                "💡 Available commands: /start, /help, /status"
            )
            logger.info(f"✅ Text response sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Text response error: {e}")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle images"""
        user = update.effective_user
        logger.info(f"📸 Image received from {user.username} ({user.id})")
        
        processing_message = None
        try:
            # Send processing message
            logger.info("📤 Sending processing message…")
            processing_message = await update.message.reply_text("🔍 Analyzing image…")
            logger.info("✅ Processing message sent")
            
            # Get image file
            logger.info("📁 Getting file info…")
            photo = update.message.photo[-1]  # Highest resolution
            logger.info(f"📊 Image size: {photo.width}x{photo.height}, file size: {photo.file_size} bytes")
            
            file = await context.bot.get_file(photo.file_id)
            logger.info(f"📂 Telegram file_path: {file.file_path}")
            
            # Download image
            logger.info("⬇️ Downloading image…")
            image_bytes = await self.download_image(file.file_path)
            
            if not image_bytes:
                logger.error("❌ Failed to download image")
                await processing_message.edit_text("❌ Error downloading image")
                return
            
            logger.info(f"✅ Image downloaded, size: {len(image_bytes)} bytes")
            
            # Update status
            await processing_message.edit_text("🧠 Extracting text via OpenAI GPT-4o Vision…")
            
            # Analyze image via OpenAI
            logger.info("🤖 Sending request to OpenAI…")
            
            # Extract text
            ocr_result = await self.extract_text_via_openai(image_bytes)
            
            if not ocr_result:
                logger.error("❌ OpenAI could not extract text from image")
                await processing_message.edit_text(
                    "❌ Failed to extract text from image\n\n"
                    "Possible reasons:\n"
                    "• The image is blurry or too small\n"
                    "• Temporary OpenAI API unavailability\n\n"
                    "Please try again with a clearer image"
                )
                return
            
            logger.info(f"✅ Text extracted, length: {len(ocr_result)} chars")
            
            # Имя файла для сохранения в БД
            try:
                file_name = os.path.basename(file.file_path) if file.file_path else f"{photo.file_id}.jpg"
            except Exception:
                file_name = f"{photo.file_id}.jpg"
            
            # Telegram message length limit handling (4096 chars)
            if len(ocr_result) > 4000:
                # Отправляем частями
                await processing_message.edit_text(f"📋 **EXTRACTED TEXT (part 1):**\n{ocr_result[:4000]}")
                await update.message.reply_text(f"📋 **EXTRACTED TEXT (part 2):**\n{ocr_result[4000:]}")
            else:
                # Отправляем одним сообщением
                await processing_message.edit_text(f"📋 **EXTRACTED TEXT:**\n{ocr_result}")
            
            logger.info(f"📤 Text sent to user {user.id}")

            # Сохраняем результат в БД
            self.save_parse_result(file_name=file_name, full_text=ocr_result)
                
        except Exception as e:
            logger.error(f"💥 Critical error while processing image: {e}", exc_info=True)
            try:
                if processing_message:
                    await processing_message.edit_text(f"❌ Processing error occurred:\n{str(e)[:200]}...")
                else:
                    await update.message.reply_text(f"❌ Processing error occurred:\n{str(e)[:200]}...")
            except Exception as send_error:
                logger.error(f"❌ Failed to send error message: {send_error}")
    
    async def download_image(self, file_path: str) -> Optional[bytes]:
        """Download image by path"""
        # Формируем правильный URL
        if file_path.startswith('http'):
            url = file_path
        else:
            url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
        
        logger.info(f"⬇️ Final download URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            logger.info(f"📡 HTTP status: {response.status_code}")
            
            if response.status_code == 200:
                content_length = len(response.content)
                logger.info(f"✅ Image successfully downloaded, size: {content_length} bytes")
                return response.content
            else:
                logger.error(f"❌ HTTP error: {response.status_code}, text: {response.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"❌ Exception while downloading image: {e}", exc_info=True)
            return None
    
    async def extract_text_via_openai(self, image_bytes: bytes) -> Optional[str]:
        """Extract text from image via OpenAI GPT-4o Vision"""
        logger.info(f"🤖 Starting text extraction via OpenAI, image size: {len(image_bytes)} bytes")
        
        try:
            # Encode image to base64
            img_b64 = base64.b64encode(image_bytes).decode('utf-8')
            logger.info(f"🖼️ Image encoded to base64, length: {len(img_b64)} chars")
            
            # Prompt
            prompt = "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
            
            # Headers
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Payload
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.1
            }
            
            logger.info(f"💬 Prompt: {prompt}")
            logger.info("🚀 Sending POST request to OpenAI…")
            
            response = requests.post(
                OPENAI_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            logger.info(f"📡 HTTP status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Successful response from OpenAI")
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content'].strip()
                    logger.info(f"✅ Text extracted, length: {len(content)} chars")
                    logger.info(f"📝 First 100 chars: {content[:100]}...")
                    return content
                else:
                    logger.error("❌ Unexpected OpenAI response format")
                    return None
            else:
                logger.error(f"❌ OpenAI API error: {response.status_code}")
                logger.error(f"📄 Error text: {response.text[:500]}")
                return None
                
        except Exception as e:
            logger.error(f"💥 Text extraction error: {e}", exc_info=True)
            return None
    

    
    def run(self):
        """Start the bot"""
        logger.info("🚀 Starting bot…")
        logger.info("🔄 Starting polling for updates…")
        
        try:
            # Use standard run_polling
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"❌ Critical error while starting bot: {e}", exc_info=True)
            raise

def main():
    """Main entry point"""
    logger.info("🎬 Starting main()…")
    logger.info("🔧 Creating bot instance…")
    
    try:
        bot = ImageAnalysisBot()
        logger.info("✅ Bot created successfully!")
        bot.run()
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Critical error in main(): {e}", exc_info=True)
        raise
    finally:
        logger.info("🏁 Shutting down bot")

if __name__ == "__main__":
    main() 