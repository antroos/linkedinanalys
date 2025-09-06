#!/usr/bin/env python3
"""
Скрипт для диагностики LLaVA HuggingFace Endpoint API
"""

import requests
import json
import os

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud")

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}

print("🔍 Диагностика LLaVA HuggingFace Endpoint")
print(f"🔗 Endpoint: {HUGGINGFACE_ENDPOINT}")
print("=" * 60)

# Тестируем разные пути и методы
test_paths = [
    "",
    "/",
    "/docs",
    "/openapi.json",
    "/predict",
    "/generate", 
    "/infer",
    "/api/predict",
    "/run/predict",
    "/v1/chat/completions",
    "/health",
    "/info"
]

for path in test_paths:
    url = HUGGINGFACE_ENDPOINT + path
    print(f"\n🎯 Тестирую: {url}")
    
    # Пробуем GET запрос
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  GET: {response.status_code}")
        if response.status_code == 200:
            try:
                content = response.json()
                print(f"  📄 JSON Response: {json.dumps(content, indent=2)[:200]}...")
            except:
                print(f"  📄 Text Response: {response.text[:100]}...")
        elif response.status_code in [404, 405]:
            print(f"  ❌ {response.status_code}: {response.text[:50]}")
        else:
            print(f"  ⚠️ {response.status_code}: {response.text[:50]}")
    except Exception as e:
        print(f"  💥 GET Error: {e}")
    
    # Пробуем POST запрос с минимальными данными
    try:
        test_data = {"test": "ping"}
        response = requests.post(url, headers=headers, json=test_data, timeout=10)
        print(f"  POST: {response.status_code}")
        if response.status_code not in [404, 405]:
            print(f"  📄 Response: {response.text[:100]}...")
    except Exception as e:
        print(f"  💥 POST Error: {e}")

print("\n" + "=" * 60)
print("🔍 Попробуем стандартный формат HuggingFace Inference API:")

# Тестируем стандартный формат HuggingFace
test_data = {
    "inputs": "What is in this image?",
    "parameters": {
        "max_new_tokens": 100
    }
}

try:
    response = requests.post(
        HUGGINGFACE_ENDPOINT, 
        headers=headers, 
        json=test_data, 
        timeout=30
    )
    print(f"📡 Стандартный формат: {response.status_code}")
    print(f"📄 Response: {response.text}")
except Exception as e:
    print(f"💥 Error: {e}")

print("\n🏁 Диагностика завершена") 