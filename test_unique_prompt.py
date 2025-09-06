#!/usr/bin/env python3
"""
Тест с уникальными ID для избежания кеширования
"""

import requests
import base64
import json
import os
import uuid

# Конфигурация (из окружения)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud/invocations")

def test_unique_prompt():
    """Тестирует промпт с уникальным ID"""
    
    # Простое тестовое изображение
    test_image_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9PJsENQAAAABJRU5ErkJggg=="
    )
    img_b64 = base64.b64encode(test_image_data).decode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Тест с уникальным ID
    unique_id = str(uuid.uuid4())[:8]
    payload = {
        "image": img_b64,
        "prompt": f"[ID:{unique_id}] Please describe what you see in this image.",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "stop": ["<|im_end|>", "</s>"]
    }
    
    print(f"🧪 Тест с уникальным ID: {unique_id}")
    print(f"📋 Промпт: {payload['prompt']}")
    
    try:
        response = requests.post(
            HUGGINGFACE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 HTTP статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Успешный ответ:")
            print(f"📄 JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            if 'choices' in result and result['choices']:
                text = result['choices'][0].get('text', '')
                print(f"🎯 Ответ модели: '{text}'")
                print(f"📊 Длина ответа: {len(text)} символов")
        else:
            print(f"❌ Ошибка {response.status_code}")
            print(f"📄 Ответ: {response.text}")
            
    except Exception as e:
        print(f"💥 Исключение: {e}")

if __name__ == "__main__":
    test_unique_prompt() 