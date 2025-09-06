#!/usr/bin/env python3
"""
Test with unique IDs to avoid caching (optional HF endpoint)
"""

import requests
import base64
import json
import uuid
import os

# Optional HF config
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud/invocations")

def test_unique_prompt():
    """Test a prompt with a unique ID"""
    
    test_image_data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChAI9PJsENQAAAABJRU5ErkJggg=="
    )
    img_b64 = base64.b64encode(test_image_data).decode('utf-8')
    
    if not HUGGINGFACE_TOKEN or not HUGGINGFACE_ENDPOINT:
        print("⚠️ Skipping: HF endpoint/token not set")
        return
    
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    unique_id = str(uuid.uuid4())[:8]
    payload = {
        "image": img_b64,
        "prompt": f"[ID:{unique_id}] Please describe what you see in this image.",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
        "stop": ["<|im_end|>", "</s>"]
    }
    
    print(f"🧪 Unique test ID: {unique_id}")
    print(f"📋 Prompt: {payload['prompt']}")
    
    try:
        response = requests.post(
            HUGGINGFACE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 HTTP status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Successful response:")
            print(f"📄 JSON: {json.dumps(result, indent=2, ensure_ascii=False)}")
            text = result.get('choices', [{}])[0].get('text', '')
            print(f"🎯 Output: '{text}'")
            print(f"📊 Length: {len(text)} chars)")
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Exception: {e}")

if __name__ == "__main__":
    test_unique_prompt() 