#!/usr/bin/env python3
"""
Скрипт настройки телеграм бота для анализа изображений
"""

import os
import sys
import subprocess

def install_dependencies():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Зависимости успешно установлены!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при установке зависимостей: {e}")
        return False

def create_env_file():
    """Создание файла .env с примером конфигурации"""
    env_file = ".env"
    
    if os.path.exists(env_file):
        print(f"📁 Файл {env_file} уже существует")
        return True
    
    env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ Создан файл {env_file}")
        print("⚠️  Не забудьте заполнить токены в файле .env!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании {env_file}: {e}")
        return False

def check_python_version():
    """Проверка версии Python"""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"❌ Требуется Python {min_version[0]}.{min_version[1]}+ (текущая версия: {current_version[0]}.{current_version[1]})")
        return False
    
    print(f"✅ Python версия {current_version[0]}.{current_version[1]} подходит")
    return True

def main():
    """Основная функция настройки"""
    print("🚀 Настройка телеграм бота для анализа изображений")
    print("=" * 50)
    
    # Проверка версии Python
    if not check_python_version():
        sys.exit(1)
    
    # Установка зависимостей
    if not install_dependencies():
        sys.exit(1)
    
    # Создание файла .env
    if not create_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Настройка завершена!")
    print("\n📋 Следующие шаги:")
    print("1. Получите токен бота от @BotFather в Telegram")
    print("2. Получите API ключ OpenAI на platform.openai.com")
    print("3. Заполните токены в файле .env")
    print("4. Запустите бота командой: python main.py")
    print("\n📖 Подробные инструкции в README.md")

if __name__ == "__main__":
    main() 