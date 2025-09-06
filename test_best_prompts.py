#!/usr/bin/env python3
"""
Тест лучших промптов для финальной проверки
"""

import requests
import base64
import json
import os
from pathlib import Path

# Конфигурация (из окружения)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud/invocations")
IMAGE_PATH = "Снимок экрана 2025-07-16 в 01.41.27.png"

# Лучшие промпты + дополнительные вариации
BEST_PROMPTS = [
    "Human: What text is visible in this image?\nAssistant:",
    "What words and text are written in this image?",
    "Human: Read all text from this image.\nAssistant:",
    "Human: What text do you see?\nAssistant:",
    "Assistant: I can see text in this image. The text says:",
    "Q: What text is in this image?\nA:",
    "Please identify all text visible in this image:",
    "Human: Can you extract the text from this image?\nAssistant:"
]

def test_best_prompt(prompt_text, prompt_index):
    """Тестирует один из лучших промптов"""
    
    print(f"\n🔥 ФИНАЛЬНЫЙ ТЕСТ #{prompt_index + 1}")
    print(f"📋 Промпт: '{prompt_text}'")
    print("-" * 70)
    
    try:
        # Загружаем изображение
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        img_b64 = base64.b64encode(image_data).decode('utf-8')
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "image": img_b64,
            "prompt": prompt_text,
            "max_tokens": 200,
            "temperature": 0.1,
            "top_p": 0.9
        }
        
        response = requests.post(
            HUGGINGFACE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and result['choices']:
                text = result['choices'][0].get('text', '').strip()
                tokens = result.get('usage', {}).get('completion_tokens', 0)
                
                print(f"✅ Токенов: {tokens}")
                print(f"📝 Ответ: '{text}'")
                
                # Оценка качества
                is_good = (
                    len(text) > 10 and 
                    not text.startswith('and ') and 
                    not text.startswith('including ') and
                    not text.startswith('with ') and
                    not text == ''
                )
                
                if is_good:
                    print(f"🎯 ОТЛИЧНЫЙ РЕЗУЛЬТАТ!")
                    return True, text
                else:
                    print(f"⚠️ Слабый результат")
                    
        else:
            print(f"❌ Ошибка {response.status_code}")
            
    except Exception as e:
        print(f"💥 Ошибка: {e}")
    
    return False, ""

def main():
    """Финальное тестирование лучших промптов"""
    
    print("🏆 ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ЛУЧШИХ ПРОМПТОВ")
    print(f"🖼️ Изображение: {IMAGE_PATH}")
    print("=" * 80)
    
    winners = []
    
    for i, prompt in enumerate(BEST_PROMPTS):
        success, response_text = test_best_prompt(prompt, i)
        if success:
            winners.append((i + 1, prompt, response_text))
    
    # Результаты
    print("\n" + "=" * 80)
    print("🏅 ПОБЕДИТЕЛИ:")
    print("=" * 80)
    
    if winners:
        for num, prompt, response in winners:
            print(f"\n#{num} ПРОМПТ: '{prompt}'")
            print(f"   ОТВЕТ: '{response}'")
    else:
        print("❌ Ни один промпт не прошел тест")
    
    # Рекомендация
    if winners:
        best_prompt = winners[0][1]  # Первый успешный
        print(f"\n🎯 РЕКОМЕНДУЕМЫЙ ПРОМПТ ДЛЯ БОТА:")
        print(f"'{best_prompt}'")

if __name__ == "__main__":
    main() 