#!/usr/bin/env python3
"""
Тест разных промптов для извлечения текста с реального изображения
"""

import requests
import base64
import json
import os
from pathlib import Path

# Конфигурация (из окружения)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud/invocations")

# Путь к изображению
IMAGE_PATH = "Снимок экрана 2025-07-16 в 01.41.27.png"

# Список промптов для тестирования
PROMPTS_TO_TEST = [
    "What text do you see in this image?",
    "Read all text from this image.",
    "Extract all visible text from this image.",
    "List all text, words, and numbers visible in this image.",
    "Transcribe all text content from this image.",
    "What words and text are written in this image?",
    "Please read and list every text element you can see.",
    "Perform OCR on this image and list all text.",
    "USER: Extract all text from this image.\nASSISTANT:",
    "Human: What text is visible in this image?\nAssistant:",
    "Image contains text. Read it all.",
    "Describe all text content in this image.",
    "Найди и перечисли весь текст на этом изображении.",
    "Какой текст написан на этой картинке?"
]

def test_prompt_with_real_image(prompt_text, prompt_index):
    """Тестирует конкретный промпт с реальным изображением"""
    
    print(f"\n🧪 ТЕСТ #{prompt_index + 1}")
    print(f"📋 Промпт: '{prompt_text}'")
    print("-" * 60)
    
    try:
        # Загружаем реальное изображение
        if not Path(IMAGE_PATH).exists():
            print(f"❌ Файл {IMAGE_PATH} не найден!")
            return
            
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        # Кодируем в base64
        img_b64 = base64.b64encode(image_data).decode('utf-8')
        print(f"🖼️ Изображение загружено: {len(image_data)} байт, base64: {len(img_b64)} символов")
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Формируем payload
        payload = {
            "image": img_b64,
            "prompt": prompt_text,
            "max_tokens": 300,
            "temperature": 0.1,
            "top_p": 0.9
        }
        
        # Отправляем запрос
        print("🚀 Отправляю запрос...")
        response = requests.post(
            HUGGINGFACE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 HTTP статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and result['choices']:
                text = result['choices'][0].get('text', '').strip()
                tokens = result.get('usage', {}).get('completion_tokens', 0)
                
                print(f"✅ УСПЕХ!")
                print(f"📊 Токенов: {tokens}")
                print(f"📝 Ответ модели:")
                print(f"    '{text}'")
                
                # Проверяем качество ответа
                if len(text) > 20 and not text.startswith('and ') and not text.startswith('including '):
                    print(f"🎯 ОТЛИЧНЫЙ РЕЗУЛЬТАТ! Полный ответ без фрагментов")
                    return True
                else:
                    print(f"⚠️ Короткий/фрагментарный ответ")
                    
            else:
                print(f"❌ Нет текста в ответе")
                
        else:
            print(f"❌ Ошибка {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            
    except Exception as e:
        print(f"💥 Исключение: {e}")
    
    return False

def main():
    """Тестирует все промпты"""
    
    print("🔥 ТЕСТИРОВАНИЕ ПРОМПТОВ ДЛЯ ИЗВЛЕЧЕНИЯ ТЕКСТА")
    print(f"🖼️ Изображение: {IMAGE_PATH}")
    print(f"🔗 Endpoint: {HUGGINGFACE_ENDPOINT}")
    print(f"📝 Количество промптов: {len(PROMPTS_TO_TEST)}")
    print("=" * 80)
    
    successful_prompts = []
    
    for i, prompt in enumerate(PROMPTS_TO_TEST):
        success = test_prompt_with_real_image(prompt, i)
        if success:
            successful_prompts.append((i + 1, prompt))
    
    # Итоги
    print("\n" + "=" * 80)
    print("🏆 ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 80)
    
    if successful_prompts:
        print(f"✅ Успешных промптов: {len(successful_prompts)}")
        for num, prompt in successful_prompts:
            print(f"   #{num}: '{prompt}'")
    else:
        print(f"❌ Ни один промпт не дал хорошего результата")
    
    print(f"\n📊 Всего протестировано: {len(PROMPTS_TO_TEST)} промптов")

if __name__ == "__main__":
    main() 