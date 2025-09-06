#!/usr/bin/env python3
"""
OpenAI GPT-4 Vision OCR test – extract text from an image
"""

import requests
import base64
import json
import os
from pathlib import Path

# OpenAI configuration (from env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Image path
IMAGE_PATH = "Снимок экрана 2025-07-16 в 01.41.27.png"

# OCR prompts
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
    """Test OpenAI GPT-4 Vision with a specific prompt"""
    
    print(f"\n🔥 OPENAI TEST #{prompt_index + 1}")
    print(f"📋 Prompt: '{prompt_text}'")
    print("-" * 80)
    
    try:
        if not Path(IMAGE_PATH).exists():
            print(f"❌ Image not found: {IMAGE_PATH}!")
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
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}}
                    ]
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        print("🚀 Sending request to OpenAI…")
        response = requests.post(
            OPENAI_API_URL,
            headers=headers,
            json=payload,
            timeout=30
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
                print("-" * 50)
                print(content)
                print("-" * 50)
                
                # Quality heuristic example
                if len(content) > 20 and ("text" in content.lower() or "image" in content.lower()):
                    print("🎯 GOOD RESULT!")
                    return True, content
                else:
                    print("⚠️ Possibly incomplete result")
                    return True, content
            else:
                print("❌ No content in response")
                print(f"📄 Full response: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"💥 Exception: {e}")
    
    return False, ""

def main():
    """Run OCR tests"""
    
    print("🚀 TESTING OPENAI GPT-4 VISION FOR OCR")
    print(f"🖼️ Image: {IMAGE_PATH}")
    print(f"🔗 API: {OPENAI_API_URL}")
    print(f"📝 Prompts: {len(OCR_PROMPTS)}")
    print("=" * 100)
    
    successful_results = []
    
    for i, prompt in enumerate(OCR_PROMPTS):
        success, response_text = test_openai_vision(prompt, i)
        if success:
            successful_results.append((i + 1, prompt, response_text))
        
        import time
        time.sleep(1)
    
    print("\n" + "=" * 100)
    print("🏆 OPENAI TEST RESULTS")
    print("=" * 100)
    
    if successful_results:
        print(f"✅ Successful: {len(successful_results)}")
        for num, prompt, response in successful_results[:3]:
            print(f"\n🎯 RESULT #{num}:")
            print(f"   PROMPT: '{prompt}'")
            print(f"   RESPONSE: {response[:200]}{'...' if len(response) > 200 else ''}")
    else:
        print("❌ No successful results")
    
    if successful_results:
        best_prompt = successful_results[0][1]
        print(f"\n🎯 RECOMMENDED PROMPT FOR BOT:")
        print(f"'{best_prompt}'")

if __name__ == "__main__":
    main() 