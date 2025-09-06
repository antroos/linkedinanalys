#!/usr/bin/env python3
"""
Integrated flow test: OpenAI OCR + Job Analysis
"""

import base64
import requests
import json
import os

# Config (from env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def encode_image(image_path):
    """Encode image to base64"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"❌ Image encoding error: {e}")
        return None

def extract_text_via_openai(image_path):
    """Extract text via OpenAI"""
    print(f"🔍 Extracting text from: {image_path}")
    
    img_b64 = encode_image(image_path)
    if not img_b64:
        return None
    
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
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.1
    }
    
    try:
        print("🚀 Sending request to OpenAI…")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        print(f"📡 HTTP status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                print(f"✅ Extracted text length: {len(content)} chars")
                return content
            else:
                print("❌ Unexpected response format")
                return None
        else:
            print(f"❌ OpenAI API error: {response.status_code}")
            print(f"📄 Error text: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"💥 Text extraction error: {e}")
        return None

def analyze_job_via_openai(extracted_text):
    """Analyze current job from extracted text"""
    print(f"🎯 Analyzing job, text length: {len(extracted_text)} chars")
    
    prompt = f"""Analyze the text below and extract ONLY the person's current job.

Return JSON:
{{
  "current_job": {{
    "company": "company name",
    "position": "position", 
    "period": "work period (if provided)",
    "is_current": true/false
  }},
  "found": true/false
}}

If you can't determine the current job, return {{"found": false}}.

TEXT:
{extracted_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.1
    }
    
    try:
        print("🚀 Sending job analysis request…")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        print(f"📡 HTTP status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                print(f"✅ Job analysis length: {len(content)} chars")
                return content
            else:
                print("❌ Unexpected analysis response")
                return None
        else:
            print(f"❌ OpenAI API analysis error: {response.status_code}")
            print(f"📄 Error: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"💥 Job analysis error: {e}")
        return None

def test_full_workflow():
    """Run full workflow test"""
    print("=" * 80)
    print("FULL FLOW TEST: OCR + JOB ANALYSIS")
    print("=" * 80)
    
    image_path = "screenshot_2025-07-15T13-58-11-498Z.jpg"
    
    print("\n🔍 STEP 1: OCR")
    print("-" * 40)
    ocr_result = extract_text_via_openai(image_path)
    
    if not ocr_result:
        print("❌ Failed to extract text")
        return
    
    print(f"📝 Extracted text (first 200 chars):")
    print(ocr_result[:200] + "..." if len(ocr_result) > 200 else ocr_result)
    
    print("\n🎯 STEP 2: JOB ANALYSIS")
    print("-" * 40)
    job_analysis = analyze_job_via_openai(ocr_result)
    
    if job_analysis:
        print(f"📊 Job analysis:")
        print(job_analysis)
    else:
        print("❌ Failed to analyze job")
    
    print("\n📋 STEP 3: FINAL MESSAGE")
    print("-" * 40)
    final_response = f"📋 **EXTRACTED TEXT:**\n{ocr_result}\n\n"
    if job_analysis:
        final_response += f"💼 **JOB ANALYSIS:**\n{job_analysis}"
    else:
        final_response += "💼 **JOB ANALYSIS:**\nNot detected"
    print(f"📏 Final message length: {len(final_response)} chars")
    if len(final_response) > 4000:
        print("⚠️ Message exceeds 4000 chars — will be split")
    else:
        print("✅ Message fits in a single Telegram message")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_full_workflow() 