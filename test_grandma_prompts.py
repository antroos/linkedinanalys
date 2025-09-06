#!/usr/bin/env python3
"""
Prompt tests with token usage for OpenAI GPT-4 Vision
"""

import requests
import base64
import json
import os
from pathlib import Path

# OpenAI configuration (from env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Same prompts for consistency testing
GRANDMA_PROMPTS = [
    {"id": 1, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 2, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 3, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 4, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 5, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 6, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 7, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 8, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 9, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
    {"id": 10, "text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers."},
]

def encode_image(image_path):
    """Encode image to base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Image encoding error: {e}")
        return None

def test_grandma_prompt(prompt_data, image_path):
    """Test prompt with OpenAI API and return token stats"""
    try:
        print(f"\n{'='*80}")
        print(f"PROMPT #{prompt_data['id']}")
        print(f"{'='*80}")
        print(f"Text: {prompt_data['text']}")
        print(f"Image: {image_path}")
        print("-" * 80)
        
        base64_image = encode_image(image_path)
        if not base64_image:
            return False, None
        
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
                        {"type": "text", "text": prompt_data['text']},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        print("🚀 Sending request to OpenAI…")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            usage = result.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            message_content = result['choices'][0]['message']['content']
            
            print("✅ SUCCESS!")
            print("📊 TOKENS:")
            print(f"   • Prompt: {prompt_tokens}")
            print(f"   • Completion: {completion_tokens}")
            print(f"   • Total: {total_tokens}")
            print("📝 RESPONSE:")
            print(f"{message_content}")
            
            return True, {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'total_tokens': total_tokens,
                'response': message_content,
                'prompt_id': prompt_data['id']
            }
        else:
            print(f"❌ HTTP ERROR {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False, None

def main():
    """Main test runner"""
    print("🚀 Running prompt tests with token usage")
    
    test_images = [
        "screenshot_2025-07-15T13-58-11-498Z.jpg"
    ]
    
    for image_path in test_images:
        print(f"\n{'#'*100}")
        print(f"TESTING IMAGE: {image_path}")
        print(f"{'#'*100}")
        
        if not Path(image_path).exists():
            print(f"❌ Image not found: {image_path}")
            continue
            
        successful_prompts = 0
        total_prompts = len(GRANDMA_PROMPTS)
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
        
        print(f"\n{'='*100}")
        print("📊 TOKEN STATS (TOTAL)")
        print(f"{'='*100}")
        print(f"✅ Successful: {successful_prompts}/{total_prompts}")
        print("📈 Totals:")
        print(f"   • Prompt tokens: {total_prompt_tokens}")
        print(f"   • Completion tokens: {total_completion_tokens}")
        print(f"   • Total tokens: {total_all_tokens}")
        
        if successful_prompts > 0:
            avg_prompt = total_prompt_tokens / successful_prompts
            avg_completion = total_completion_tokens / successful_prompts
            avg_total = total_all_tokens / successful_prompts
            print("📊 Averages per successful request:")
            print(f"   • Prompt: {avg_prompt:.1f}")
            print(f"   • Completion: {avg_completion:.1f}")
            print(f"   • Total: {avg_total:.1f}")
            # Rough cost example (update with current pricing as needed)
            input_cost = (total_prompt_tokens / 1_000_000) * 2.50
            output_cost = (total_completion_tokens / 1_000_000) * 10.00
            total_cost = input_cost + output_cost
            print("💰 Approx. cost (USD):")
            print(f"   • Input: ${input_cost:.6f}")
            print(f"   • Output: ${output_cost:.6f}")
            print(f"   • Total: ${total_cost:.6f}")
        
        print(f"\n🎯 RESULT: {successful_prompts}/{total_prompts} successful requests")

if __name__ == "__main__":
    main() 