#!/usr/bin/env python3
"""
Тест промптов с подсчетом токенов для OpenAI GPT-4 Vision
"""

import requests
import base64
import json
import os
from pathlib import Path

# Конфигурация OpenAI (из окружения)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Тест одинакового промпта для проверки консистентности
GRANDMA_PROMPTS = [
    {
        "id": 1,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 2,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 3,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 4,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 5,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 6,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 7,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 8,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 9,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    },
    {
        "id": 10,
        "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    }
]

def encode_image(image_path):
    """Кодирует изображение в base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Ошибка кодирования изображения: {e}")
        return None

def test_grandma_prompt(prompt_data, image_path):
    """Тестирует промпт с OpenAI API и возвращает статистику токенов"""
    try:
        print(f"\n{'='*80}")
        print(f"ПРОМПТ #{prompt_data['id']}")
        print(f"{'='*80}")
        print(f"Текст: {prompt_data['text']}")
        print(f"Изображение: {image_path}")
        print("-" * 80)
        
        # Кодируем изображение
        base64_image = encode_image(image_path)
        if not base64_image:
            return False, None
        
        # Подготавливаем запрос
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt_data['text']
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        print("🚀 Отправляем запрос в OpenAI...")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            
            # Извлекаем информацию о токенах
            usage = result.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            
            # Извлекаем ответ
            message_content = result['choices'][0]['message']['content']
            
            print("✅ УСПЕХ!")
            print(f"📊 СТАТИСТИКА ТОКЕНОВ:")
            print(f"   • Входящие токены (prompt): {prompt_tokens}")
            print(f"   • Исходящие токены (completion): {completion_tokens}")
            print(f"   • Всего токенов: {total_tokens}")
            print(f"📝 ОТВЕТ:")
            print(f"{message_content}")
            
            return True, {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'response': message_content,
                'prompt_id': prompt_data['id']
            }
            
        else:
            print(f"❌ ОШИБКА HTTP {response.status_code}")
            print(f"Ответ: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ ИСКЛЮЧЕНИЕ: {e}")
        return False, None

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования промптов с подсчетом токенов")
    
    # Тестируем только один файл
    test_images = [
        "screenshot_2025-07-15T13-58-11-498Z.jpg"
    ]
    
    for image_path in test_images:
        print(f"\n{'#'*100}")
        print(f"ТЕСТИРОВАНИЕ ИЗОБРАЖЕНИЯ: {image_path}")
        print(f"{'#'*100}")
        
        if not Path(image_path).exists():
            print(f"❌ Изображение не найдено: {image_path}")
            continue
            
        successful_prompts = 0
        total_prompts = len(GRANDMA_PROMPTS)
        
        # Статистика токенов
        all_token_stats = []
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_all_tokens = 0
        
        for prompt_data in GRANDMA_PROMPTS:
            success, token_stats = test_grandma_prompt(prompt_data, image_path)
            if success and token_stats:
                successful_prompts += 1
                all_token_stats.append(token_stats)
                total_prompt_tokens += token_stats['prompt_tokens']
                total_completion_tokens += token_stats['completion_tokens']
                total_all_tokens += token_stats['total_tokens']
        
        # Итоговая статистика
        print(f"\n{'='*100}")
        print(f"📊 ИТОГОВАЯ СТАТИСТИКА ТОКЕНОВ")
        print(f"{'='*100}")
        print(f"✅ Успешных запросов: {successful_prompts}/{total_prompts}")
        print(f"📈 Общая статистика токенов:")
        print(f"   • Всего входящих токенов: {total_prompt_tokens}")
        print(f"   • Всего исходящих токенов: {total_completion_tokens}")
        print(f"   • Общий расход токенов: {total_all_tokens}")
        
        if successful_prompts > 0:
            avg_prompt = total_prompt_tokens / successful_prompts
            avg_completion = total_completion_tokens / successful_prompts
            avg_total = total_all_tokens / successful_prompts
            
            print(f"📊 Средние значения на запрос:")
            print(f"   • Средние входящие токены: {avg_prompt:.1f}")
            print(f"   • Средние исходящие токены: {avg_completion:.1f}")
            print(f"   • Средний общий расход: {avg_total:.1f}")
            
            # Приблизительная стоимость (актуальные цены GPT-4o на январь 2025)
            # Input: $2.50 per 1M tokens, Output: $10.00 per 1M tokens
            input_cost = (total_prompt_tokens / 1_000_000) * 2.50
            output_cost = (total_completion_tokens / 1_000_000) * 10.00
            total_cost = input_cost + output_cost
            
            print(f"💰 Приблизительная стоимость (USD):")
            print(f"   • Входящие токены: ${input_cost:.6f}")
            print(f"   • Исходящие токены: ${output_cost:.6f}")
            print(f"   • Общая стоимость: ${total_cost:.6f}")
        
        print(f"\n🎯 РЕЗУЛЬТАТ: {successful_prompts}/{total_prompts} успешных запросов")

if __name__ == "__main__":
    main() 