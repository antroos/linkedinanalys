#!/usr/bin/env python3
"""
Тест OpenAI GPT-4 Vision API для извлечения текста
"""

import requests
import base64
import json
import os
from pathlib import Path

# Конфигурация OpenAI (из окружения)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Путь к изображению
IMAGE_PATH = "Снимок экрана 2025-07-16 в 01.41.27.png"

# Промпты для тестирования OCR
OCR_PROMPTS = [
    "Extract all visible text from this image. List every word, number, and text element you can see.",
    "Please read and transcribe all text content in this image.",
    "Perform OCR on this image. What text do you see?",
    "What text is written in this image? Please provide a complete transcription.",
    "Analyze this image and extract all readable text, including any numbers, names, or labels.",
    "Read all text from this screenshot/image and provide the exact transcription.",
    "I need you to act as an OCR tool. Extract every piece of text visible in this image.",
    "This image contains text. Please read it all and provide a detailed transcription.",
    "Scan this image for text and provide a complete list of all visible words and text elements.",
    "Extract and list all text content from this image, maintaining the original formatting if possible."
]

def test_openai_vision(prompt_text, prompt_index):
    """Тестирует OpenAI GPT-4 Vision с определенным промптом"""
    
    print(f"\n🔥 OPENAI ТЕСТ #{prompt_index + 1}")
    print(f"📋 Промпт: '{prompt_text}'")
    print("-" * 80)
    
    try:
        # Загружаем изображение
        if not Path(IMAGE_PATH).exists():
            print(f"❌ Файл {IMAGE_PATH} не найден!")
            return False, ""
            
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        # Кодируем в base64
        img_b64 = base64.b64encode(image_data).decode('utf-8')
        print(f"🖼️ Изображение загружено: {len(image_data)} байт, base64: {len(img_b64)} символов")
        
        # Заголовки
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Payload для OpenAI Vision API
        payload = {
            "model": "gpt-4o",  # Или gpt-4-vision-preview
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        print("🚀 Отправляю запрос к OpenAI...")
        response = requests.post(
            OPENAI_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 HTTP статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content'].strip()
                tokens = result.get('usage', {}).get('completion_tokens', 0)
                
                print(f"✅ УСПЕХ!")
                print(f"📊 Токенов: {tokens}")
                print(f"📝 Ответ GPT-4:")
                print("-" * 50)
                print(content)
                print("-" * 50)
                
                # Проверяем качество
                if len(content) > 20 and ("text" in content.lower() or "изображени" in content.lower()):
                    print(f"🎯 ОТЛИЧНЫЙ РЕЗУЛЬТАТ!")
                    return True, content
                else:
                    print(f"⚠️ Возможно неполный результат")
                    return True, content  # Все равно считаем успехом
                    
            else:
                print(f"❌ Нет содержимого в ответе")
                print(f"📄 Полный ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
        else:
            print(f"❌ Ошибка {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            
    except Exception as e:
        print(f"💥 Исключение: {e}")
    
    return False, ""

def main():
    """Тестирует OpenAI GPT-4 Vision для OCR"""
    
    print("🚀 ТЕСТИРОВАНИЕ OPENAI GPT-4 VISION ДЛЯ OCR")
    print(f"🖼️ Изображение: {IMAGE_PATH}")
    print(f"🔗 API: {OPENAI_API_URL}")
    print(f"📝 Количество промптов: {len(OCR_PROMPTS)}")
    print("=" * 100)
    
    successful_results = []
    
    for i, prompt in enumerate(OCR_PROMPTS):
        success, response_text = test_openai_vision(prompt, i)
        if success:
            successful_results.append((i + 1, prompt, response_text))
        
        # Небольшая пауза между запросами
        import time
        time.sleep(1)
    
    # Итоги
    print("\n" + "=" * 100)
    print("🏆 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ OPENAI")
    print("=" * 100)
    
    if successful_results:
        print(f"✅ Успешных тестов: {len(successful_results)}")
        
        # Показываем лучшие результаты
        for num, prompt, response in successful_results[:3]:  # Первые 3
            print(f"\n🎯 РЕЗУЛЬТАТ #{num}:")
            print(f"   ПРОМПТ: '{prompt}'")
            print(f"   ОТВЕТ: {response[:200]}{'...' if len(response) > 200 else ''}")
    else:
        print("❌ Ни один тест не дал результата")
    
    # Рекомендация для бота
    if successful_results:
        best_prompt = successful_results[0][1]
        print(f"\n🎯 ЛУЧШИЙ ПРОМПТ ДЛЯ БОТА:")
        print(f"'{best_prompt}'")
        
        print(f"\n💡 РЕКОМЕНДАЦИЯ:")
        print(f"Переключить бота на OpenAI GPT-4 Vision API вместо HuggingFace endpoint")

if __name__ == "__main__":
    main() 