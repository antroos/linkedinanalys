#!/usr/bin/env python3
"""
Тест выбранных промптов OpenAI GPT-4 Vision на новом изображении
"""

import requests
import base64
import json
import os
from pathlib import Path

# Конфигурация OpenAI (из окружения)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Новое изображение
IMAGE_PATH = "screenshot_2025-07-15T13-58-11-498Z.jpg"

# Выбранные промпты (1, 5, 7, 8, 9, 10)
SELECTED_PROMPTS = [
    {
        "id": 1,
        "text": "Extract all visible text from this image. List every word, number, and text element you can see."
    },
    {
        "id": 5,
        "text": "Analyze this image and extract all readable text, including any numbers, names, or labels."
    },
    {
        "id": 7,
        "text": "I need you to act as an OCR tool. Extract every piece of text visible in this image."
    },
    {
        "id": 8,
        "text": "This image contains text. Please read it all and provide a detailed transcription."
    },
    {
        "id": 9,
        "text": "Scan this image for text and provide a complete list of all visible words and text elements."
    },
    {
        "id": 10,
        "text": "Extract and list all text content from this image, maintaining the original formatting if possible."
    }
]

def test_selected_prompt(prompt_data):
    """Тестирует выбранный промпт на новом изображении"""
    
    prompt_id = prompt_data["id"]
    prompt_text = prompt_data["text"]
    
    print(f"\n🔥 ТЕСТ #{prompt_id}")
    print(f"📋 Промпт: '{prompt_text}'")
    print("=" * 100)
    
    try:
        # Проверяем существование файла
        if not Path(IMAGE_PATH).exists():
            print(f"❌ Файл {IMAGE_PATH} не найден!")
            return False, ""
            
        # Загружаем изображение
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
            "model": "gpt-4o",
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
                                "url": f"data:image/jpeg;base64,{img_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1500,
            "temperature": 0.1
        }
        
        print("🚀 Отправляю запрос к OpenAI...")
        response = requests.post(
            OPENAI_API_URL,
            headers=headers,
            json=payload,
            timeout=45
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
                print("─" * 100)
                print(content)
                print("─" * 100)
                
                return True, content
                    
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
    """Тестирует выбранные промпты на новом изображении"""
    
    print("🎯 ТЕСТИРОВАНИЕ ВЫБРАННЫХ ПРОМПТОВ НА НОВОМ ИЗОБРАЖЕНИИ")
    print(f"🖼️ Изображение: {IMAGE_PATH}")
    print(f"🔗 API: {OPENAI_API_URL}")
    print(f"📝 Количество промптов: {len(SELECTED_PROMPTS)}")
    print("=" * 120)
    
    results = []
    
    for prompt_data in SELECTED_PROMPTS:
        success, response_text = test_selected_prompt(prompt_data)
        if success:
            results.append((prompt_data["id"], prompt_data["text"], response_text))
        
        # Пауза между запросами
        import time
        time.sleep(2)
    
    # Итоги
    print("\n" + "=" * 120)
    print("🏆 ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 120)
    
    if results:
        print(f"✅ Успешных тестов: {len(results)} из {len(SELECTED_PROMPTS)}")
        
        for prompt_id, prompt_text, response in results:
            print(f"\n🎯 ПРОМПТ #{prompt_id} - УСПЕХ")
            print(f"   Текст: '{prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}'")
            print(f"   Длина ответа: {len(response)} символов")
    else:
        print("❌ Ни один тест не дал результата")

if __name__ == "__main__":
    main() 