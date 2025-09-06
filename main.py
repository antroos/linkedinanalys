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

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация токенов (из переменных окружения)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

logger.info("🤖 Инициализация бота...")

# Проверка токенов
if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN не установлен!")
    sys.exit(1)
else:
    logger.info(f"✅ Telegram токен загружен (длина: {len(TELEGRAM_TOKEN)} символов)")

if not OPENAI_API_KEY:
    logger.error("❌ OPENAI_API_KEY не установлен!")
    sys.exit(1)
else:
    logger.info(f"✅ OpenAI токен загружен (длина: {len(OPENAI_API_KEY)} символов)")
    logger.info(f"🔗 OpenAI API URL: {OPENAI_API_URL}")

class ImageAnalysisBot:
    def __init__(self):
        logger.info("🔧 Создание экземпляра бота...")
        try:
            # Создаем application с обычным Updater
            self.application = Application.builder().token(TELEGRAM_TOKEN).build()
            logger.info("✅ Telegram Application создан")
            # Инициализируем БД для хранения результатов парсинга
            self.db_path = 'image_analysis_results.db'
            self.init_db()
            self.setup_handlers()
            logger.info("✅ Обработчики настроены")
        except Exception as e:
            logger.error(f"❌ Ошибка создания бота: {e}")
            raise
    
    def setup_handlers(self):
        """Настройка обработчиков команд и сообщений"""
        logger.info("⚙️ Настройка обработчиков...")
        
        # Обработчики команд
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("results", self.results_command))
        self.application.add_handler(CommandHandler("export", self.export_command))
        
        # Обработчики сообщений
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        
        logger.info("✅ Все обработчики добавлены")
    
    def init_db(self):
        """Создает таблицу для хранения результатов парсинга, если ее нет"""
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
            logger.info("🗄️ База данных и таблица file_parse_results готовы")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации БД: {e}", exc_info=True)

    def save_parse_result(self, file_name: str, full_text: str):
        """Сохраняет результат парсинга в БД"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO file_parse_results (file_name, full_text) VALUES (?, ?)',
                (file_name, full_text)
            )
            conn.commit()
            conn.close()
            logger.info("💾 Результат сохранен в БД: %s", file_name)
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения результата в БД: {e}", exc_info=True)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        logger.info(f"📝 Команда /start от {user.username} ({user.id})")
        
        welcome_message = (
            f"👋 Hello, {user.first_name}!\n\n"
            "🖼️ I extract text from images using OpenAI GPT-4o Vision!\n\n"
            "📷 Send me any image with text, and I will:\n"
            "• Extract all text and numbers from the image\n"
            "• Provide clean text results\n\n"
            "💡 Available commands:\n"
            "• /start - Show this message\n"
            "• /help - Help guide\n"
            "• /status - Bot status"
        )
        
        try:
            await update.message.reply_text(welcome_message)
            logger.info(f"✅ Welcome message sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки приветствия: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        user = update.effective_user
        logger.info(f"📚 Команда /help от {user.username} ({user.id})")
        
        help_message = (
            "🆘 Bot Usage Guide:\n\n"
            "📷 **Text Extraction from Images:**\n"
            "• Send any image with text\n"
            "• Get all extracted text and numbers\n"
            "• Support for any images containing text\n\n"
            "🔧 **Technical Details:**\n"
            "• AI Model: OpenAI GPT-4o Vision\n"
            "• OCR: High-precision text extraction\n"
            "• Maximum size: 20MB\n"
            "• Supported formats: JPG, PNG, PDF\n\n"
            "❓ **Commands:**\n"
            "• /start - Start working\n"
            "• /help - This help guide\n"
            "• /status - Check status"
        )
        
        try:
            await update.message.reply_text(help_message, parse_mode='Markdown')
            logger.info(f"✅ Help guide sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки справки: {e}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /status"""
        user = update.effective_user
        logger.info(f"⚡ Команда /status от {user.username} ({user.id})")
        
        status_message = (
            "🟢 Bot is working normally!\n\n"
            "🔧 **Component Status:**\n"
            "• Telegram API: ✅ Connected\n"
            "• OpenAI API: ✅ Available\n"
            "• GPT-4o Vision: ✅ Active\n\n"
            "📊 **Information:**\n"
            "• AI Model: OpenAI GPT-4o Vision\n"
            "• Function: OCR (text extraction)\n"
            "• Bot Version: 4.1"
        )
        
        try:
            await update.message.reply_text(status_message)
            logger.info(f"✅ Status sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Ошибка отправки статуса: {e}")
    
    async def results_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать последние 5 записей парсинга (имя файла, длина текста, дата)"""
        user = update.effective_user
        logger.info(f"📚 Команда /results от {user.username} ({user.id})")

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
                await update.message.reply_text("Поки що записів немає. Надішли зображення для парсингу.")
                return

            lines = ["Останні результати (макс. 5):\n"]
            for rid, fname, tlen, ts in rows:
                lines.append(f"#{rid} | {ts} | {fname} | {tlen} символів")

            await update.message.reply_text("\n".join(lines))
            logger.info("✅ Результати отправлены пользователю %s", user.id)
        except Exception as e:
            logger.error(f"❌ Ошибка команды /results: {e}", exc_info=True)
            await update.message.reply_text("❌ Помилка при читанні бази. Спробуй ще раз пізніше.")

    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Экспорт всех результатов в CSV и отправка как файл"""
        user = update.effective_user
        logger.info(f"📚 Команда /export от {user.username} ({user.id})")

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
                await update.message.reply_text("Поки що немає даних для експорту.")
                return

            # Формируем CSV в памяти
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["parsed_at", "file_name", "full_text"])
            for parsed_at, file_name, full_text in rows:
                writer.writerow([parsed_at, file_name, full_text])

            data = csv_buffer.getvalue().encode('utf-8')
            csv_bytes = BytesIO(data)
            filename = f"file_parse_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            await update.message.reply_document(document=csv_bytes, filename=filename)
            logger.info("✅ CSV экспорт отправлен пользователю %s", user.id)
        except Exception as e:
            logger.error(f"❌ Ошибка команды /export: {e}", exc_info=True)
            await update.message.reply_text("❌ Помилка при експорті. Спробуй ще раз пізніше.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user = update.effective_user
        logger.info(f"💬 Текстовое сообщение от {user.username} ({user.id}): {update.message.text[:50]}...")
        
        try:
            await update.message.reply_text(
                "📷 Send me an image with text!\n\n"
                "🔍 I will extract all text and numbers from the image\n\n"
                "💡 Available commands: /start, /help, /status"
            )
            logger.info(f"✅ Text response sent to user {user.id}")
        except Exception as e:
            logger.error(f"❌ Ошибка ответа на текст: {e}")
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик изображений"""
        user = update.effective_user
        logger.info(f"📸 Получено изображение от {user.username} ({user.id})")
        
        processing_message = None
        try:
            # Отправляем сообщение о начале обработки
            logger.info("📤 Отправляю сообщение о начале обработки...")
            processing_message = await update.message.reply_text("🔍 Analyzing image...")
            logger.info("✅ Сообщение о начале обработки отправлено")
            
            # Получаем файл изображения
            logger.info("📁 Получаю информацию о файле...")
            photo = update.message.photo[-1]  # Берем наибольшее разрешение
            logger.info(f"📊 Размер изображения: {photo.width}x{photo.height}, размер файла: {photo.file_size} байт")
            
            file = await context.bot.get_file(photo.file_id)
            logger.info(f"📂 Telegram file_path: {file.file_path}")
            
            # Скачиваем изображение
            logger.info("⬇️ Скачиваю изображение...")
            image_bytes = await self.download_image(file.file_path)
            
            if not image_bytes:
                logger.error("❌ Не удалось скачать изображение")
                await processing_message.edit_text("❌ Error downloading image")
                return
            
            logger.info(f"✅ Изображение скачано, размер: {len(image_bytes)} байт")
            
            # Обновляем статус
            await processing_message.edit_text("🧠 Extracting text from image via OpenAI GPT-4o Vision...")
            
            # Анализируем изображение через OpenAI
            logger.info("🤖 Отправляю запрос в OpenAI...")
            
            # Извлечение текста
            ocr_result = await self.extract_text_via_openai(image_bytes)
            
            if not ocr_result:
                logger.error("❌ OpenAI не смог извлечь текст из изображения")
                await processing_message.edit_text(
                    "❌ Failed to extract text from image\n\n"
                    "Possible reasons:\n"
                    "• Image is blurry or too small\n"
                    "• Temporary OpenAI API unavailability\n\n"
                    "Please try again with a clearer image"
                )
                return
            
            logger.info(f"✅ Текст извлечен, длина: {len(ocr_result)} символов")
            
            # Имя файла для сохранения в БД
            try:
                file_name = os.path.basename(file.file_path) if file.file_path else f"{photo.file_id}.jpg"
            except Exception:
                file_name = f"{photo.file_id}.jpg"
            
            # Проверяем длину сообщения (лимит Telegram 4096 символов)
            if len(ocr_result) > 4000:
                # Отправляем частями
                await processing_message.edit_text(f"📋 **EXTRACTED TEXT (part 1):**\n{ocr_result[:4000]}")
                await update.message.reply_text(f"📋 **EXTRACTED TEXT (part 2):**\n{ocr_result[4000:]}")
            else:
                # Отправляем одним сообщением
                await processing_message.edit_text(f"📋 **EXTRACTED TEXT:**\n{ocr_result}")
            
            logger.info(f"📤 Текст отправлен пользователю {user.id}")

            # Сохраняем результат в БД
            self.save_parse_result(file_name=file_name, full_text=ocr_result)
                
        except Exception as e:
            logger.error(f"💥 Критическая ошибка при обработке изображения: {e}", exc_info=True)
            try:
                if processing_message:
                    await processing_message.edit_text(f"❌ Processing error occurred:\n{str(e)[:200]}...")
                else:
                    await update.message.reply_text(f"❌ Processing error occurred:\n{str(e)[:200]}...")
            except Exception as send_error:
                logger.error(f"❌ Не удалось отправить сообщение об ошибке: {send_error}")
    
    async def download_image(self, file_path: str) -> Optional[bytes]:
        """Скачивает изображение по пути"""
        # Формируем правильный URL
        if file_path.startswith('http'):
            url = file_path
        else:
            url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
        
        logger.info(f"⬇️ Финальный URL для скачивания: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            logger.info(f"📡 HTTP статус: {response.status_code}")
            
            if response.status_code == 200:
                content_length = len(response.content)
                logger.info(f"✅ Изображение успешно скачано, размер: {content_length} байт")
                return response.content
            else:
                logger.error(f"❌ Ошибка HTTP: {response.status_code}, текст: {response.text[:200]}")
                return None
        except Exception as e:
            logger.error(f"❌ Исключение при скачивании изображения: {e}", exc_info=True)
            return None
    
    async def extract_text_via_openai(self, image_bytes: bytes) -> Optional[str]:
        """Извлекает текст из изображения через OpenAI GPT-4o Vision"""
        logger.info(f"🤖 Начинаю извлечение текста через OpenAI, размер изображения: {len(image_bytes)} байт")
        
        try:
            # Кодируем изображение в base64
            img_b64 = base64.b64encode(image_bytes).decode('utf-8')
            logger.info(f"🖼️ Изображение закодировано в base64, длина: {len(img_b64)} символов")
            
            # Наш проверенный промпт
            prompt = "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
            
            # Подготавливаем заголовки
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # Подготавливаем payload
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
            
            logger.info(f"💬 Промпт: {prompt}")
            logger.info("🚀 Отправляю POST запрос в OpenAI...")
            
            response = requests.post(
                OPENAI_API_URL,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            logger.info(f"📡 HTTP статус: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Получен успешный ответ от OpenAI")
                
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content'].strip()
                    logger.info(f"✅ Текст извлечен, длина: {len(content)} символов")
                    logger.info(f"📝 Первые 100 символов: {content[:100]}...")
                    return content
                else:
                    logger.error("❌ Неожиданный формат ответа от OpenAI")
                    return None
            else:
                logger.error(f"❌ Ошибка OpenAI API: {response.status_code}")
                logger.error(f"📄 Текст ошибки: {response.text[:500]}")
                return None
                
        except Exception as e:
            logger.error(f"💥 Ошибка при извлечении текста: {e}", exc_info=True)
            return None
    

    
    def run(self):
        """Запуск бота"""
        logger.info("🚀 Запускаю бота...")
        logger.info("🔄 Начинаю polling для получения обновлений...")
        
        try:
            # Используем стандартный run_polling
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Exception as e:
            logger.error(f"❌ Критическая ошибка при запуске бота: {e}", exc_info=True)
            raise

def main():
    """Главная функция"""
    logger.info("🎬 Запуск главной функции...")
    logger.info("🔧 Создаю экземпляр бота...")
    
    try:
        bot = ImageAnalysisBot()
        logger.info("✅ Бот создан успешно!")
        bot.run()
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка в main(): {e}", exc_info=True)
        raise
    finally:
        logger.info("🏁 Завершение работы бота")

if __name__ == "__main__":
    main() 