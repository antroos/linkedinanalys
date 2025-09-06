#!/usr/bin/env python3
"""
Test various prompts for text extraction on a real image (optional HF endpoint)
"""

import requests
import base64
import json
import os
from pathlib import Path

# Optional HF config via env
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud/invocations")

# Image path
IMAGE_PATH = "Снимок экрана 2025-07-16 в 01.41.27.png"

PROMPTS_TO_TEST = [
    "What text do you see in this image?",
    "Read all text from this image.",
    "Extract all visible text from this image.",
    "List all text, words, and numbers visible in this image.",
    "Transcribe all text content from this image.",
    "Please read and list every text element you can see.",
    "Perform OCR on this image and list all text.",
    "USER: Extract all text from this image.\nASSISTANT:",
    "Human: What text is visible in this image?\nAssistant:",
    "Image contains text. Read it all.",
    "Describe all text content in this image.",
]

def test_prompt_with_real_image(prompt_text, prompt_index):
    """Test a prompt against a real image (HF endpoint if configured)"""
    
    print(f"\n🧪 TEST #{prompt_index + 1}")
    print(f"📋 Prompt: '{prompt_text}'")
    print("-" * 60)
    
    try:
        if not Path(IMAGE_PATH).exists():
            print(f"❌ Image not found: {IMAGE_PATH}")
            return False
        
        with open(IMAGE_PATH, "rb") as f:
            image_data = f.read()
        
        img_b64 = base64.b64encode(image_data).decode('utf-8')
        print(f"🖼️ Image loaded: {len(image_data)} bytes, base64: {len(img_b64)} chars")
        
        if not HUGGINGFACE_TOKEN or not HUGGINGFACE_ENDPOINT:
            print("⚠️ Skipping: HF endpoint/token not set")
            return False
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "image": img_b64,
            "prompt": prompt_text,
            "max_tokens": 300,
            "temperature": 0.1,
            "top_p": 0.9
        }
        
        print("🚀 Sending request…")
        response = requests.post(
            HUGGINGFACE_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 HTTP status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            text = result.get('choices', [{}])[0].get('text', '').strip()
            tokens = result.get('usage', {}).get('completion_tokens', 0)
            print("✅ SUCCESS!")
            print(f"📊 Tokens: {tokens}")
            print("📝 Model output:")
            print(f"    '{text}'")
            return len(text) > 20
        else:
            print(f"❌ Error {response.status_code}")
            print(f"📄 Response: {response.text}")
    except Exception as e:
        print(f"💥 Exception: {e}")
    
    return False

def main():
    """Run all prompts"""
    
    print("🔥 TESTING PROMPTS FOR TEXT EXTRACTION")
    print(f"🖼️ Image: {IMAGE_PATH}")
    print(f"🔗 Endpoint: {HUGGINGFACE_ENDPOINT}")
    print(f"📝 Prompts: {len(PROMPTS_TO_TEST)}")
    print("=" * 80)
    
    successful_prompts = []
    
    for i, prompt in enumerate(PROMPTS_TO_TEST):
        success = test_prompt_with_real_image(prompt, i)
        if success:
            successful_prompts.append((i + 1, prompt))
    
    print("\n" + "=" * 80)
    print("🏆 TEST RESULTS")
    print("=" * 80)
    
    if successful_prompts:
        print(f"✅ Successful: {len(successful_prompts)}")
        for num, prompt in successful_prompts:
            print(f"   #{num}: '{prompt}'")
    else:
        print("ℹ️ No successful prompts (endpoint not configured or no good outputs)")
    
    print(f"\n📊 Total tested: {len(PROMPTS_TO_TEST)} prompts")

if __name__ == "__main__":
    main() 