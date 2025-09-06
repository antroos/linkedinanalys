#!/usr/bin/env python3
"""
Тест інтегрованого флоу: OpenAI OCR + Job Analysis
"""

import base64
import requests
import json
import os

# Конфігурація (ключ з оточення)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def encode_image(image_path):
    """Кодує зображення в base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Помилка кодування зображення: {e}")
        return None

def extract_text_via_openai(image_path):
    """Витягує текст з зображення через OpenAI"""
    print(f"🔍 Витягування тексту з: {image_path}")
    
    # Кодуємо зображення
    img_b64 = encode_image(image_path)
    if not img_b64:
        return None
    
    # Наш перевірений промпт
    prompt = "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."
    
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
    
    try:
        print("🚀 Відправляю запит до OpenAI...")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        
        print(f"📡 HTTP статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                print(f"✅ Текст витягнуто, довжина: {len(content)} символів")
                return content
            else:
                print("❌ Неочікуваний формат відповіді")
                return None
        else:
            print(f"❌ Помилка OpenAI API: {response.status_code}")
            print(f"📄 Текст помилки: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"💥 Помилка при витягуванні тексту: {e}")
        return None

def analyze_job_via_openai(extracted_text):
    """Аналізує місце роботи з витягнутого тексту"""
    print(f"🎯 Аналіз місця роботи, довжина тексту: {len(extracted_text)} символів")
    
    prompt = f"""Проанализируй текст ниже и извлеки ТОЛЬКО текущее место работы человека.

Мне нужна информация в формате JSON:
{{
  "current_job": {{
    "company": "название компании",
    "position": "должность", 
    "period": "период работы (если указан)",
    "is_current": true/false
  }},
  "found": true/false
}}

Ищи ключевые слова: "Present", "Current", "Founder", "CEO", "Head of", или другие указания на текущую работу.
Если не можешь определить текущую работу, верни {{"found": false}}.

ТЕКСТ ДЛЯ АНАЛИЗА:
{extracted_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 200,
        "temperature": 0.1
    }
    
    try:
        print("🚀 Відправляю запит аналізу роботи...")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        
        print(f"📡 HTTP статус аналізу: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                print(f"✅ Аналіз завершено, довжина: {len(content)} символів")
                return content
            else:
                print("❌ Неочікуваний формат відповіді аналізу")
                return None
        else:
            print(f"❌ Помилка OpenAI API аналізу: {response.status_code}")
            print(f"📄 Текст помилки: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"💥 Помилка при аналізі роботи: {e}")
        return None

def test_full_workflow():
    """Тестує повний флоу"""
    print("=" * 80)
    print("ТЕСТ ПОВНОГО ФЛОУ: OCR + АНАЛІЗ РОБОТИ")
    print("=" * 80)
    
    # Тестове зображення
    image_path = "screenshot_2025-07-15T13-58-11-498Z.jpg"
    
    # Крок 1: Витягування тексту
    print("\n🔍 КРОК 1: ВИТЯГУВАННЯ ТЕКСТУ")
    print("-" * 40)
    ocr_result = extract_text_via_openai(image_path)
    
    if not ocr_result:
        print("❌ Не вдалося витягти текст")
        return
    
    print(f"📝 Витягнутий текст (перші 200 символів):")
    print(ocr_result[:200] + "..." if len(ocr_result) > 200 else ocr_result)
    
    # Крок 2: Аналіз роботи
    print("\n🎯 КРОК 2: АНАЛІЗ МІСЦЯ РОБОТИ")
    print("-" * 40)
    job_analysis = analyze_job_via_openai(ocr_result)
    
    if job_analysis:
        print(f"📊 Аналіз роботи:")
        print(job_analysis)
    else:
        print("❌ Не вдалося проаналізувати місце роботи")
    
    # Крок 3: Форматування результату (як у боті)
    print("\n📋 КРОК 3: ФІНАЛЬНИЙ РЕЗУЛЬТАТ")
    print("-" * 40)
    
    final_response = f"📋 **ВИТЯГНУТИЙ ТЕКСТ:**\n{ocr_result}\n\n"
    
    if job_analysis:
        final_response += f"💼 **АНАЛІЗ МІСЦЯ РОБОТИ:**\n{job_analysis}"
    else:
        final_response += "💼 **АНАЛІЗ МІСЦЯ РОБОТИ:**\nНе вдалося визначити поточне місце роботи"
    
    print(f"📏 Довжина фінального повідомлення: {len(final_response)} символів")
    
    if len(final_response) > 4000:
        print("⚠️ Повідомлення довше за 4000 символів - буде розділено")
    else:
        print("✅ Повідомлення помістится в один Telegram message")
    
    print("\n" + "=" * 80)
    print("ТЕСТ ЗАВЕРШЕНО")
    print("=" * 80)

if __name__ == "__main__":
    test_full_workflow() 