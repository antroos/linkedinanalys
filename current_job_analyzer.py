#!/usr/bin/env python3
"""
Current job analyzer via OpenAI API
Extracts the current job from each analysis and tracks changes
"""

import sqlite3
import requests
import json
from datetime import datetime
import os

# OpenAI configuration (from env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def extract_current_job_via_openai(response_text, analysis_id):
    """Extract current job via OpenAI API"""
    
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

Look for keywords like: "Present", "Current", "Founder", "CEO", "Head of", etc.
If you can't determine the current job, return {{"found": false}}.

TEXT TO ANALYZE:
{response_text}
"""

    try:
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
            "max_tokens": 300,
            "temperature": 0.1
        }
        
        print(f"🔍 Analyzing job in analysis #{analysis_id}...")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            
            # Try to parse JSON
            try:
                cleaned_response = ai_response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()
                elif cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response.replace("```", "").strip()
                
                job_data = json.loads(cleaned_response)
                return job_data
            except json.JSONDecodeError:
                print(f"⚠️  JSON parse failed for analysis #{analysis_id}")
                print(f"OpenAI response: {ai_response}")
                return {"found": False, "error": "JSON parse failed", "raw_response": ai_response}
        
        else:
            print(f"❌ OpenAI API error: {response.status_code}")
            return {"found": False, "error": f"API error {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Exception analyzing #{analysis_id}: {e}")
        return {"found": False, "error": str(e)}

def analyze_all_jobs():
    """Analyze current job across successful analyses"""
    
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, response_text
        FROM analysis_results 
        WHERE status = 'SUCCESS'
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    print("🏢 CURRENT JOB ANALYZER")
    print("="*80)
    print(f"Found {len(results)} successful analyses to process")
    
    job_extractions = []
    
    for result in results:
        analysis_id, response_text = result
        job_info = extract_current_job_via_openai(response_text, analysis_id)
        job_extractions.append({
            "analysis_id": analysis_id,
            "job_info": job_info,
            "timestamp": datetime.now().isoformat()
        })
        print(f"\n📋 ANALYSIS #{analysis_id}:")
        if job_info.get("found", False):
            current_job = job_info.get("current_job", {})
            print(f"   🏢 Company: {current_job.get('company', 'N/A')}")
            print(f"   👔 Position: {current_job.get('position', 'N/A')}")
            print(f"   📅 Period: {current_job.get('period', 'N/A')}")
            print(f"   ✅ Current: {current_job.get('is_current', 'Unknown')}")
        else:
            print(f"   ❌ Current job not found")
            if "error" in job_info:
                print(f"   🔴 Error: {job_info['error']}")
    
    return job_extractions

def compare_job_changes(job_extractions):
    """Compare job changes across analyses"""
    
    print(f"\n{'='*80}")
    print("🔄 JOB CHANGES ANALYSIS")
    print("="*80)
    
    found_jobs = [job for job in job_extractions if job["job_info"].get("found", False)]
    
    if len(found_jobs) < 2:
        print("❌ Not enough data to compare (need at least 2)")
        return
    
    print(f"📊 Comparing {len(found_jobs)} extracted jobs:")
    
    companies = []
    positions = []
    
    for job in found_jobs:
        current_job = job["job_info"]["current_job"]
        company = current_job.get("company", "").strip().lower()
        position = current_job.get("position", "").strip().lower()
        
        if company:
            companies.append((job["analysis_id"], company))
        if position:
            positions.append((job["analysis_id"], position))
    
    print(f"\n🏢 COMPANY CHANGES:")
    unique_companies = list(set([comp[1] for comp in companies]))
    
    if len(unique_companies) == 1:
        print(f"   ✅ Company unchanged: {unique_companies[0]}")
    else:
        print(f"   🔄 Detected {len(unique_companies)} different companies:")
        for i, company in enumerate(unique_companies, 1):
            analyses = [comp[0] for comp in companies if comp[1] == company]
            print(f"      {i}. '{company}' (analyses: {', '.join(map(str, analyses))})")
    
    print(f"\n👔 POSITION CHANGES:")
    unique_positions = list(set([pos[1] for pos in positions]))
    
    if len(unique_positions) == 1:
        print(f"   ✅ Position unchanged: {unique_positions[0]}")
    else:
        print(f"   🔄 Detected {len(unique_positions)} different positions:")
        for i, position in enumerate(unique_positions, 1):
            analyses = [pos[0] for pos in positions if pos[1] == position]
            print(f"      {i}. '{position}' (analyses: {', '.join(map(str, analyses))})")

def save_job_analysis_results(job_extractions):
    """Save analysis results to JSON file"""
    
    output_data = {
        "analysis_timestamp": datetime.now().isoformat(),
        "total_analyses": len(job_extractions),
        "successful_extractions": len([job for job in job_extractions if job["job_info"].get("found", False)]),
        "job_extractions": job_extractions
    }
    
    filename = f"job_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Saved results to: {filename}")
    return filename

def create_summary_report(job_extractions):
    """Create summary report"""
    
    found_jobs = [job for job in job_extractions if job["job_info"].get("found", False)]
    
    print(f"\n{'='*80}")
    print("📊 SUMMARY REPORT")
    print("="*80)
    
    print(f"📈 Overall:")
    print(f"   • Processed analyses: {len(job_extractions)}")
    print(f"   • Found current job: {len(found_jobs)}")
    print(f"   • Not found: {len(job_extractions) - len(found_jobs)}")
    print(f"   • Success rate: {len(found_jobs)/len(job_extractions)*100:.1f}%")
    
    if found_jobs:
        companies = [job["job_info"]["current_job"].get("company", "").strip().lower() 
                    for job in found_jobs if job["job_info"]["current_job"].get("company")]
        
        if companies:
            from collections import Counter
            company_counts = Counter(companies)
            most_common_company = company_counts.most_common(1)[0]
            
            print(f"\n🏢 Companies:")
            print(f"   • Total mentions: {len(companies)}")
            print(f"   • Unique companies: {len(set(companies))}")
            print(f"   • Most common: '{most_common_company[0]}' ({most_common_company[1]} times)")
            
            if len(set(companies)) > 1:
                print(f"   ⚠️  NOTE: Different companies detected — possible job change.")
            else:
                print(f"   ✅ Company is consistent across analyses")

def main():
    """Entrypoint"""
    
    print("🏢 CURRENT JOB ANALYZER")
    print("="*60)
    print("Uses OpenAI API to extract current job from image analysis responses")
    print()
    
    try:
        job_extractions = analyze_all_jobs()
        compare_job_changes(job_extractions)
        create_summary_report(job_extractions)
        filename = save_job_analysis_results(job_extractions)
        
        print(f"\n✅ Analysis completed!")
        print(f"📁 Details: {filename}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main() 