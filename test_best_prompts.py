#!/usr/bin/env python3
"""
Final prompt tests – example scaffold (requires Hugging Face endpoint/token set via env if used)
"""

import requests
import base64
import json
import os
from pathlib import Path

# Optional Hugging Face config via env (kept empty by default to avoid secrets)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
HUGGINGFACE_ENDPOINT = os.getenv("HUGGINGFACE_ENDPOINT", "https://example.huggingface.cloud/invocations")
IMAGE_PATH = "Снимок экрана 2025-07-16 в 01.41.27.png"

BEST_PROMPTS = [
    "What text is visible in this image?",
    "Read all text from this image.",
    "Extract the text from this image.",
]

def test_best_prompt(prompt_text, prompt_index):
    """Test a prompt against an inference endpoint (if configured)"""
    
    print(f"\n🔥 FINAL TEST #{prompt_index + 1}")
    print(f"📋 Prompt: '{prompt_text}'")
    print("-" * 70)
    
    try:
        if not HUGGINGFACE_TOKEN or not HUGGINGFACE_ENDPOINT:
            print("⚠️ Skipping: HF endpoint/token not set (HUGGINGFACE_TOKEN / HUGGINGFACE_ENDPOINT)")
            return False, ""
        
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
            text = result.get('choices', [{}])[0].get('text', '').strip()
            tokens = result.get('usage', {}).get('completion_tokens', 0)
            print(f"✅ Tokens: {tokens}")
            print(f"📝 Output: '{text}'")
            is_good = len(text) > 10
            return is_good, text
        else:
            print(f"❌ HTTP {response.status_code}")
            return False, ""
    except Exception as e:
        print(f"💥 Error: {e}")
        return False, ""

def main():
    """Run final prompt tests (optional HF example)"""
    
    print("🏆 FINAL PROMPT TESTS")
    print(f"🖼️ Image: {IMAGE_PATH}")
    print("=" * 80)
    
    winners = []
    
    for i, prompt in enumerate(BEST_PROMPTS):
        success, response_text = test_best_prompt(prompt, i)
        if success:
            winners.append((i + 1, prompt, response_text))
    
    print("\n" + "=" * 80)
    print("🏅 WINNERS:")
    print("=" * 80)
    
    if winners:
        for num, prompt, response in winners:
            print(f"\n#{num} PROMPT: '{prompt}'")
            print(f"   OUTPUT: '{response}'")
        best_prompt = winners[0][1]
        print(f"\n🎯 RECOMMENDED PROMPT FOR BOT:")
        print(best_prompt)
    else:
        print("ℹ️ No winners (endpoint not configured or no good outputs)")

if __name__ == "__main__":
    main() 