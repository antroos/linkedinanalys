#!/usr/bin/env python3
"""
Анализатор текущего места работы через OpenAI API
Извлекает текущую работу из каждого анализа и отслеживает изменения
"""

import sqlite3
import requests
import json
from datetime import datetime
import os

# Конфигурация OpenAI (из окружения)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def extract_current_job_via_openai(response_text, analysis_id):
    """Извлекает текущее место работы через OpenAI API"""
    
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
        
        print(f"🔍 Анализируем работу в анализе #{analysis_id}...")
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            
            # Пытаемся парсить JSON ответ
            try:
                # Убираем markdown форматирование если есть
                cleaned_response = ai_response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response.replace("```json", "").replace("```", "").strip()
                elif cleaned_response.startswith("```"):
                    cleaned_response = cleaned_response.replace("```", "").strip()
                
                job_data = json.loads(cleaned_response)
                return job_data
            except json.JSONDecodeError:
                # Если не удалось парсить JSON, извлекаем информацию вручную
                print(f"⚠️  Не удалось парсить JSON для анализа #{analysis_id}")
                print(f"Ответ OpenAI: {ai_response}")
                return {"found": False, "error": "JSON parse failed", "raw_response": ai_response}
        
        else:
            print(f"❌ Ошибка OpenAI API: {response.status_code}")
            return {"found": False, "error": f"API error {response.status_code}"}
            
    except Exception as e:
        print(f"❌ Исключение при анализе #{analysis_id}: {e}")
        return {"found": False, "error": str(e)}

def analyze_all_jobs():
    """Анализирует текущую работу во всех успешных анализах"""
    
    # Подключаемся к базе данных
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    # Получаем все успешные анализы
    cursor.execute('''
        SELECT analysis_id, response_text
        FROM analysis_results 
        WHERE status = 'SUCCESS'
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    print("🏢 АНАЛИЗ ТЕКУЩИХ МЕСТ РАБОТЫ")
    print("="*80)
    print(f"Найдено {len(results)} успешных анализов для обработки")
    
    job_extractions = []
    
    for result in results:
        analysis_id, response_text = result
        
        # Извлекаем информацию о работе через OpenAI
        job_info = extract_current_job_via_openai(response_text, analysis_id)
        
        job_extractions.append({
            "analysis_id": analysis_id,
            "job_info": job_info,
            "timestamp": datetime.now().isoformat()
        })
        
        # Показываем результат
        print(f"\n📋 АНАЛИЗ #{analysis_id}:")
        if job_info.get("found", False):
            current_job = job_info.get("current_job", {})
            print(f"   🏢 Компания: {current_job.get('company', 'Не указана')}")
            print(f"   👔 Должность: {current_job.get('position', 'Не указана')}")
            print(f"   📅 Период: {current_job.get('period', 'Не указан')}")
            print(f"   ✅ Текущая: {current_job.get('is_current', 'Неизвестно')}")
        else:
            print(f"   ❌ Текущая работа не найдена")
            if "error" in job_info:
                print(f"   🔴 Ошибка: {job_info['error']}")
    
    return job_extractions

def compare_job_changes(job_extractions):
    """Сравнивает изменения в работе между анализами"""
    
    print(f"\n{'='*80}")
    print("🔄 АНАЛИЗ ИЗМЕНЕНИЙ В РАБОТЕ")
    print("="*80)
    
    # Фильтруем только найденные работы
    found_jobs = [job for job in job_extractions if job["job_info"].get("found", False)]
    
    if len(found_jobs) < 2:
        print("❌ Недостаточно данных для сравнения (нужно минимум 2 успешных извлечения)")
        return
    
    print(f"📊 Сравниваем {len(found_jobs)} извлеченных мест работы:")
    
    # Группируем по компаниям и должностям
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
    
    # Анализируем изменения в компании
    print(f"\n🏢 АНАЛИЗ ИЗМЕНЕНИЙ КОМПАНИИ:")
    unique_companies = list(set([comp[1] for comp in companies]))
    
    if len(unique_companies) == 1:
        print(f"   ✅ Компания не менялась: {unique_companies[0]}")
    else:
        print(f"   🔄 Обнаружено {len(unique_companies)} разных компаний:")
        for i, company in enumerate(unique_companies, 1):
            analyses = [comp[0] for comp in companies if comp[1] == company]
            print(f"      {i}. '{company}' (анализы: {', '.join(map(str, analyses))})")
    
    # Анализируем изменения в должности
    print(f"\n👔 АНАЛИЗ ИЗМЕНЕНИЙ ДОЛЖНОСТИ:")
    unique_positions = list(set([pos[1] for pos in positions]))
    
    if len(unique_positions) == 1:
        print(f"   ✅ Должность не менялась: {unique_positions[0]}")
    else:
        print(f"   🔄 Обнаружено {len(unique_positions)} разных должностей:")
        for i, position in enumerate(unique_positions, 1):
            analyses = [pos[0] for pos in positions if pos[1] == position]
            print(f"      {i}. '{position}' (анализы: {', '.join(map(str, analyses))})")

def save_job_analysis_results(job_extractions):
    """Сохраняет результаты анализа в JSON файл"""
    
    output_data = {
        "analysis_timestamp": datetime.now().isoformat(),
        "total_analyses": len(job_extractions),
        "successful_extractions": len([job for job in job_extractions if job["job_info"].get("found", False)]),
        "job_extractions": job_extractions
    }
    
    filename = f"job_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результаты сохранены в: {filename}")
    return filename

def create_summary_report(job_extractions):
    """Создает итоговый отчет"""
    
    found_jobs = [job for job in job_extractions if job["job_info"].get("found", False)]
    
    print(f"\n{'='*80}")
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("="*80)
    
    print(f"📈 Общая статистика:")
    print(f"   • Всего анализов обработано: {len(job_extractions)}")
    print(f"   • Успешно извлечена работа: {len(found_jobs)}")
    print(f"   • Не удалось извлечь: {len(job_extractions) - len(found_jobs)}")
    print(f"   • Процент успеха: {len(found_jobs)/len(job_extractions)*100:.1f}%")
    
    if found_jobs:
        # Самая частая компания
        companies = [job["job_info"]["current_job"].get("company", "").strip().lower() 
                    for job in found_jobs if job["job_info"]["current_job"].get("company")]
        
        if companies:
            from collections import Counter
            company_counts = Counter(companies)
            most_common_company = company_counts.most_common(1)[0]
            
            print(f"\n🏢 Информация о компаниях:")
            print(f"   • Всего упоминаний компаний: {len(companies)}")
            print(f"   • Уникальных компаний: {len(set(companies))}")
            print(f"   • Самая частая: '{most_common_company[0]}' ({most_common_company[1]} раз)")
            
            if len(set(companies)) > 1:
                print(f"   ⚠️  ВНИМАНИЕ: Обнаружены разные компании! Возможна смена работы.")
            else:
                print(f"   ✅ Компания стабильна во всех анализах")

def main():
    """Основная функция"""
    
    print("🏢 АНАЛИЗАТОР ТЕКУЩЕГО МЕСТА РАБОТЫ")
    print("="*60)
    print("Использует OpenAI API для извлечения информации о работе")
    print("из результатов анализа изображений")
    print()
    
    try:
        # Анализируем все места работы
        job_extractions = analyze_all_jobs()
        
        # Сравниваем изменения
        compare_job_changes(job_extractions)
        
        # Создаем итоговый отчет
        create_summary_report(job_extractions)
        
        # Сохраняем результаты
        filename = save_job_analysis_results(job_extractions)
        
        print(f"\n✅ Анализ завершен!")
        print(f"📁 Подробные результаты: {filename}")
        
    except Exception as e:
        print(f"❌ Ошибка при выполнении анализа: {e}")

if __name__ == "__main__":
    main() 