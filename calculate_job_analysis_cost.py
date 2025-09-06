#!/usr/bin/env python3
"""
Подсчет стоимости анализа работы через OpenAI API
"""

import json
import sqlite3

# Тарифы OpenAI GPT-4o (актуальные на январь 2025)
OPENAI_PRICING = {
    "input_cost_per_1m_tokens": 2.50,   # $2.50 за 1M входящих токенов
    "output_cost_per_1m_tokens": 10.00  # $10.00 за 1M исходящих токенов
}

def estimate_tokens_for_job_analysis():
    """Оценка токенов для анализа работы"""
    
    # Получаем данные из базы для оценки
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, response_text, prompt_tokens, completion_tokens, total_tokens
        FROM analysis_results 
        WHERE status = 'SUCCESS'
        ORDER BY analysis_id
        LIMIT 3
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("❌ Нет данных для анализа")
        return
    
    print("🧮 РАСЧЕТ СТОИМОСТИ АНАЛИЗА РАБОТЫ")
    print("="*70)
    
    # Оценим размер промпта для анализа работы
    sample_prompt = """Проанализируй текст ниже и извлеки ТОЛЬКО текущее место работы человека.

Мне нужна информация в формате JSON:
{
  "current_job": {
    "company": "название компании",
    "position": "должность", 
    "period": "период работы (если указан)",
    "is_current": true/false
  },
  "found": true/false
}

Ищи ключевые слова: "Present", "Current", "Founder", "CEO", "Head of", или другие указания на текущую работу.
Если не можешь определить текущую работу, верни {"found": false}.

ТЕКСТ ДЛЯ АНАЛИЗА:
"""
    
    # Примерная длина промпта (в символах)
    base_prompt_length = len(sample_prompt)
    
    print(f"📝 Анализ компонентов промпта:")
    print(f"   • Базовый промпт: ~{base_prompt_length} символов")
    
    # Анализируем длину ответов из базы
    total_response_length = 0
    total_original_tokens = 0
    
    for result in results:
        analysis_id, response_text, prompt_tokens, completion_tokens, total_tokens = result
        total_response_length += len(response_text)
        total_original_tokens += total_tokens
        print(f"   • Анализ #{analysis_id}: {len(response_text)} символов → {total_tokens} токенов")
    
    avg_response_length = total_response_length / len(results)
    avg_original_tokens = total_original_tokens / len(results)
    
    print(f"\n📊 Средние значения:")
    print(f"   • Средняя длина ответа: {avg_response_length:.0f} символов")
    print(f"   • Средние токены (оригинал): {avg_original_tokens:.0f}")
    
    # Оценка токенов для анализа работы
    # Грубая формула: 1 токен ≈ 4 символа для английского текста
    estimated_input_tokens_per_analysis = (base_prompt_length + avg_response_length) / 4
    estimated_output_tokens_per_analysis = 100  # JSON ответ обычно короткий
    estimated_total_tokens_per_analysis = estimated_input_tokens_per_analysis + estimated_output_tokens_per_analysis
    
    print(f"\n🔢 ОЦЕНКА ТОКЕНОВ ДЛЯ АНАЛИЗА РАБОТЫ:")
    print(f"   • Входящие токены: ~{estimated_input_tokens_per_analysis:.0f}")
    print(f"   • Исходящие токены: ~{estimated_output_tokens_per_analysis}")
    print(f"   • Всего токенов: ~{estimated_total_tokens_per_analysis:.0f}")
    
    # Расчет стоимости
    input_cost_per_analysis = (estimated_input_tokens_per_analysis / 1_000_000) * OPENAI_PRICING['input_cost_per_1m_tokens']
    output_cost_per_analysis = (estimated_output_tokens_per_analysis / 1_000_000) * OPENAI_PRICING['output_cost_per_1m_tokens']
    total_cost_per_analysis = input_cost_per_analysis + output_cost_per_analysis
    
    print(f"\n💰 СТОИМОСТЬ ОДНОГО АНАЛИЗА РАБОТЫ:")
    print(f"   • Входящие токены: ${input_cost_per_analysis:.6f}")
    print(f"   • Исходящие токены: ${output_cost_per_analysis:.6f}")
    print(f"   • Общая стоимость: ${total_cost_per_analysis:.6f}")
    
    return {
        'estimated_input_tokens': estimated_input_tokens_per_analysis,
        'estimated_output_tokens': estimated_output_tokens_per_analysis,
        'estimated_total_tokens': estimated_total_tokens_per_analysis,
        'cost_per_analysis': total_cost_per_analysis
    }

def calculate_batch_costs(cost_per_analysis):
    """Расчет стоимости для разных объемов"""
    
    print(f"\n📈 СТОИМОСТЬ ДЛЯ РАЗНЫХ ОБЪЕМОВ:")
    print("-"*70)
    
    volumes = [
        (10, "Наш тест"),
        (100, "Средний клиент/день"),
        (1000, "Крупный клиент/день"),
        (5000, "Наш клиент/неделя"),
        (21650, "Наш клиент/месяц (5000*4.33)"),
        (260000, "Наш клиент/год")
    ]
    
    for volume, description in volumes:
        total_cost = volume * cost_per_analysis
        print(f"   • {volume:6,} анализов ({description:20s}): ${total_cost:.4f}")

def compare_with_original_ocr():
    """Сравнение с оригинальным OCR анализом"""
    
    # Данные из оригинального теста
    original_cost_per_request = 0.054715 / 9  # $0.054715 за 9 успешных запросов
    
    job_analysis_data = estimate_tokens_for_job_analysis()
    if not job_analysis_data:
        return
    
    job_analysis_cost = job_analysis_data['cost_per_analysis']
    
    print(f"\n⚖️  СРАВНЕНИЕ СТОИМОСТИ:")
    print("-"*70)
    print(f"   📸 Оригинальный OCR анализ: ${original_cost_per_request:.6f}")
    print(f"   🏢 Анализ работы:           ${job_analysis_cost:.6f}")
    print(f"   📊 Разница:                ${job_analysis_cost - original_cost_per_request:.6f}")
    print(f"   📈 Увеличение:             {(job_analysis_cost/original_cost_per_request - 1)*100:.1f}%")
    
    # Общая стоимость: OCR + анализ работы
    total_cost_per_image = original_cost_per_request + job_analysis_cost
    print(f"\n💡 ОБЩАЯ СТОИМОСТЬ (OCR + анализ работы): ${total_cost_per_image:.6f}")
    
    # Для клиента с 5000 запросов в неделю
    weekly_requests = 5000
    monthly_requests = weekly_requests * 4.33
    
    monthly_ocr_cost = monthly_requests * original_cost_per_request
    monthly_job_analysis_cost = monthly_requests * job_analysis_cost
    monthly_total_cost = monthly_requests * total_cost_per_image
    
    print(f"\n🎯 ДЛЯ КЛИЕНТА (5000 запросов/неделю = {monthly_requests:.0f}/месяц):")
    print(f"   📸 OCR анализ:      ${monthly_ocr_cost:.2f}/месяц")
    print(f"   🏢 Анализ работы:   ${monthly_job_analysis_cost:.2f}/месяц")
    print(f"   📊 ИТОГО:           ${monthly_total_cost:.2f}/месяц")

def main():
    print("💼 КАЛЬКУЛЯТОР СТОИМОСТИ АНАЛИЗА РАБОТЫ")
    print("="*70)
    
    # Оценка стоимости одного анализа
    job_analysis_data = estimate_tokens_for_job_analysis()
    
    if job_analysis_data:
        # Расчет для разных объемов
        calculate_batch_costs(job_analysis_data['cost_per_analysis'])
        
        # Сравнение с оригинальным OCR
        compare_with_original_ocr()
    
    print(f"\n" + "="*70)
    print("✅ РАСЧЕТ ЗАВЕРШЕН")

if __name__ == "__main__":
    main() 