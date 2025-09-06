#!/usr/bin/env python3
"""
Test selected OpenAI GPT-4 Vision prompts on a new image
"""

import requests
import base64
import json
import os
from pathlib import Path

# OpenAI configuration (from env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# New image
IMAGE_PATH = "screenshot_2025-07-15T13-58-11-498Z.jpg"

# Selected prompts (ids)
SELECTED_PROMPTS = [
    {"id": 1, "text": "Extract all visible text from this image. List every word, number, and text element you can see."},
    {"id": 5, "text": "Analyze this image and extract all readable text, including any numbers, names, or labels."},
    {"id": 7, "text": "I need you to act as an OCR tool. Extract every piece of text visible in this image."},
    {"id": 8, "text": "This image contains text. Please read it all and provide a detailed transcription."},
    {"id": 9, "text": "Scan this image for text and provide a complete list of all visible words and text elements."},
    {"id": 10, "text": "Extract and list all text content from this image, maintaining the original formatting if possible."},
]

def test_selected_prompt(prompt_data):
    """Test a selected prompt on the image"""
    prompt_id = prompt_data["id"]
    prompt_text = prompt_data["text"]
    
    print(f"\n🔥 TEST #{prompt_id}")
    print(f"📋 Prompt: '{prompt_text}'")
    print("=" * 100)
    
    try:
        if not Path(IMAGE_PATH).exists():
            print(f"❌ Image not found: {IMAGE_PATH}")
            return False, ""
        
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        img_b64 = base64.b64encode(image_data).decode('utf-8')
        print(f"🖼️ Image loaded: {len(image_data)} bytes, base64: {len(img_b64)} chars")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]
                }
            ],
            "max_tokens": 1500,
            "temperature": 0.1
        }
        
        print("🚀 Sending request to OpenAI…")
        response = requests.post(
            OPENAI_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )
        
        print(f"📡 HTTP status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content'].strip()
                tokens = result.get('usage', {}).get('completion_tokens', 0)
                
                print("✅ SUCCESS!")
                print(f"📊 Tokens: {tokens}")
                print("📝 Response:")
                print("─" * 100)
                print(content)
                print("─" * 100)
                
                return True, content
            else:
                print("❌ No content in response")
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Exception: {e}")
    
    return False, ""

def main():
    """Run tests for selected prompts"""
    
    print("🎯 TESTING SELECTED PROMPTS ON NEW IMAGE")
    print(f"🖼️ Image: {IMAGE_PATH}")
    print(f"🔗 API: {OPENAI_API_URL}")
    print(f"📝 Number of prompts: {len(SELECTED_PROMPTS)}")
    print("=" * 120)
    
    results = []
    
    for prompt_data in SELECTED_PROMPTS:
        success, response_text = test_selected_prompt(prompt_data)
        if success:
            results.append((prompt_data["id"], prompt_data["text"], response_text))
        
        import time
        time.sleep(2)
    
    print("\n" + "=" * 120)
    print("🏆 RESULTS")
    print("=" * 120)
    
    if results:
        print(f"✅ Successful tests: {len(results)} out of {len(SELECTED_PROMPTS)}")
        for prompt_id, prompt_text, response in results:
            print(f"\n🎯 PROMPT #{prompt_id} - SUCCESS")
            print(f"   Text: '{prompt_text[:80]}{'...' if len(prompt_text) > 80 else ''}'")
            print(f"   Response length: {len(response)} chars")
    else:
        print("❌ No successful results")

if __name__ == "__main__":
    main() 