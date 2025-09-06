#!/usr/bin/env python3
"""
Калькулятор юнит-экономики для клиента
Расчет стоимости обработки изображений через OpenAI GPT-4o Vision
"""

import math

# ДАННЫЕ ИЗ ТЕСТИРОВАНИЯ (из результатов test_grandma_prompts.py)
# ===============================================================

# Статистика из реального теста 10 запросов
TEST_RESULTS = {
    "total_requests": 10,
    "successful_requests": 9,
    "failed_requests": 1,
    "success_rate": 0.9,  # 90%
    
    # Токены (из итоговой статистики)
    "total_prompt_tokens": 7182,
    "total_completion_tokens": 3676,
    "total_tokens": 10858,
    
    # Средние значения на успешный запрос
    "avg_prompt_tokens": 798.0,
    "avg_completion_tokens": 408.4,
    "avg_total_tokens": 1206.4,
    
    # Реальная стоимость 10 тестовых запросов
    "total_cost_usd": 0.054715
}

# ТАРИФЫ OPENAI GPT-4O (актуальные на январь 2025)
# ================================================
OPENAI_PRICING = {
    "input_cost_per_1m_tokens": 2.50,   # $2.50 за 1M входящих токенов
    "output_cost_per_1m_tokens": 10.00  # $10.00 за 1M исходящих токенов
}

# ТРЕБОВАНИЯ КЛИЕНТА
# ==================
CLIENT_REQUIREMENTS = {
    "requests_per_week": 5000,
    "retry_rate": 0.20,  # 20% запросов нужно переделывать
    "weeks_per_month": 4.33,  # Среднее количество недель в месяце
    "months_per_year": 12
}

def calculate_unit_economics():
    """Расчет юнит-экономики для клиента"""
    
    print("🧮 КАЛЬКУЛЯТОР ЮНИТ-ЭКОНОМИКИ")
    print("=" * 70)
    print(f"📊 Базовые данные из тестирования:")
    print(f"   • Успешность запросов: {TEST_RESULTS['success_rate']*100:.1f}%")
    print(f"   • Средние токены на запрос: {TEST_RESULTS['avg_total_tokens']:.1f}")
    print(f"   • Стоимость одного успешного запроса: ${TEST_RESULTS['total_cost_usd']/TEST_RESULTS['successful_requests']:.6f}")
    
    print(f"\n👤 Требования клиента:")
    print(f"   • Запросов в неделю: {CLIENT_REQUIREMENTS['requests_per_week']:,}")
    print(f"   • Процент переделок: {CLIENT_REQUIREMENTS['retry_rate']*100:.0f}%")
    
    # РАСЧЕТЫ
    # =======
    
    # 1. Базовое количество запросов
    base_requests_per_week = CLIENT_REQUIREMENTS['requests_per_week']
    
    # 2. Дополнительные запросы из-за переделок (20%)
    retry_requests_per_week = base_requests_per_week * CLIENT_REQUIREMENTS['retry_rate']
    
    # 3. Общее количество запросов с учетом переделок
    total_requests_per_week = base_requests_per_week + retry_requests_per_week
    
    # 4. Учитываем процент неуспешных запросов
    # Если success_rate = 90%, то нужно делать больше запросов для получения нужного результата
    adjusted_requests_per_week = total_requests_per_week / TEST_RESULTS['success_rate']
    
    # 5. Стоимость одного успешного запроса (из реальных данных)
    cost_per_successful_request = TEST_RESULTS['total_cost_usd'] / TEST_RESULTS['successful_requests']
    
    # 6. Расчет стоимости
    weekly_cost = adjusted_requests_per_week * cost_per_successful_request
    monthly_cost = weekly_cost * CLIENT_REQUIREMENTS['weeks_per_month']
    yearly_cost = monthly_cost * CLIENT_REQUIREMENTS['months_per_year']
    
    # 7. Расчет токенов
    weekly_tokens = adjusted_requests_per_week * TEST_RESULTS['avg_total_tokens']
    monthly_tokens = weekly_tokens * CLIENT_REQUIREMENTS['weeks_per_month']
    yearly_tokens = monthly_tokens * CLIENT_REQUIREMENTS['months_per_year']
    
    # ДЕТАЛЬНАЯ РАЗБИВКА ПО ТИПАМ ТОКЕНОВ
    # ===================================
    weekly_prompt_tokens = adjusted_requests_per_week * TEST_RESULTS['avg_prompt_tokens']
    weekly_completion_tokens = adjusted_requests_per_week * TEST_RESULTS['avg_completion_tokens']
    
    monthly_prompt_tokens = weekly_prompt_tokens * CLIENT_REQUIREMENTS['weeks_per_month']
    monthly_completion_tokens = weekly_completion_tokens * CLIENT_REQUIREMENTS['weeks_per_month']
    
    # Стоимость по типам токенов
    weekly_input_cost = (weekly_prompt_tokens / 1_000_000) * OPENAI_PRICING['input_cost_per_1m_tokens']
    weekly_output_cost = (weekly_completion_tokens / 1_000_000) * OPENAI_PRICING['output_cost_per_1m_tokens']
    
    monthly_input_cost = weekly_input_cost * CLIENT_REQUIREMENTS['weeks_per_month']
    monthly_output_cost = weekly_output_cost * CLIENT_REQUIREMENTS['weeks_per_month']
    
    # ВЫВОД РЕЗУЛЬТАТОВ
    # ================
    
    print(f"\n📈 ДЕТАЛЬНЫЙ РАСЧЕТ:")
    print(f"   • Базовые запросы в неделю: {base_requests_per_week:,}")
    print(f"   • Переделки (20%): {retry_requests_per_week:,.0f}")
    print(f"   • Итого с переделками: {total_requests_per_week:,.0f}")
    print(f"   • С учетом success rate (90%): {adjusted_requests_per_week:,.0f}")
    
    print(f"\n💰 СТОИМОСТЬ:")
    print(f"   📅 Неделя:")
    print(f"      • Общая стоимость: ${weekly_cost:.2f}")
    print(f"      • Входящие токены: ${weekly_input_cost:.2f}")
    print(f"      • Исходящие токены: ${weekly_output_cost:.2f}")
    
    print(f"   📅 Месяц:")
    print(f"      • Общая стоимость: ${monthly_cost:.2f}")
    print(f"      • Входящие токены: ${monthly_input_cost:.2f}")
    print(f"      • Исходящие токены: ${monthly_output_cost:.2f}")
    
    print(f"   📅 Год:")
    print(f"      • Общая стоимость: ${yearly_cost:.2f}")
    
    print(f"\n🔢 ПОТРЕБЛЕНИЕ ТОКЕНОВ:")
    print(f"   📅 Неделя: {weekly_tokens:,.0f} токенов")
    print(f"   📅 Месяц: {monthly_tokens:,.0f} токенов")
    print(f"   📅 Год: {yearly_tokens:,.0f} токенов")
    
    print(f"\n📊 ЮНИТ-МЕТРИКИ:")
    print(f"   • Стоимость одного успешного анализа: ${cost_per_successful_request:.6f}")
    print(f"   • Стоимость одного запроса с учетом переделок: ${cost_per_successful_request * 1.2:.6f}")
    print(f"   • Токенов на один успешный анализ: {TEST_RESULTS['avg_total_tokens']:.0f}")
    
    # ПРОГНОЗЫ ПРИ РАЗНЫХ ОБЪЕМАХ
    # ===========================
    
    print(f"\n🔮 ПРОГНОЗЫ ПРИ РАЗНЫХ ОБЪЕМАХ (месячная стоимость):")
    
    volumes = [1000, 2500, 5000, 10000, 20000]
    
    for volume in volumes:
        vol_adjusted = (volume + volume * CLIENT_REQUIREMENTS['retry_rate']) / TEST_RESULTS['success_rate']
        vol_weekly_cost = vol_adjusted * cost_per_successful_request
        vol_monthly_cost = vol_weekly_cost * CLIENT_REQUIREMENTS['weeks_per_month']
        
        print(f"   • {volume:,} запросов/неделю → ${vol_monthly_cost:.2f}/месяц")
    
    # РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ
    # ===========================
    
    print(f"\n💡 РЕКОМЕНДАЦИИ ПО ОПТИМИЗАЦИИ:")
    
    # Экономия от снижения retry rate
    optimized_retry_rate = 0.10  # 10% вместо 20%
    optimized_total = (base_requests_per_week + base_requests_per_week * optimized_retry_rate) / TEST_RESULTS['success_rate']
    optimized_weekly_cost = optimized_total * cost_per_successful_request
    optimized_monthly_cost = optimized_weekly_cost * CLIENT_REQUIREMENTS['weeks_per_month']
    
    savings_monthly = monthly_cost - optimized_monthly_cost
    savings_yearly = savings_monthly * 12
    
    print(f"   • Снижение переделок с 20% до 10%:")
    print(f"     - Экономия в месяц: ${savings_monthly:.2f}")
    print(f"     - Экономия в год: ${savings_yearly:.2f}")
    
    # Анализ основных трат
    input_percentage = (monthly_input_cost / monthly_cost) * 100
    output_percentage = (monthly_output_cost / monthly_cost) * 100
    
    print(f"   • Структура расходов:")
    print(f"     - Входящие токены (изображения): {input_percentage:.1f}%")
    print(f"     - Исходящие токены (ответы): {output_percentage:.1f}%")
    
    if output_percentage > 70:
        print(f"   ⚠️  Основные траты на исходящие токены!")
        print(f"     - Рекомендация: оптимизировать длину ответов")
        print(f"     - Использовать max_tokens для ограничения ответа")
    
    return {
        'weekly_cost': weekly_cost,
        'monthly_cost': monthly_cost,
        'yearly_cost': yearly_cost,
        'weekly_tokens': weekly_tokens,
        'monthly_tokens': monthly_tokens,
        'cost_per_request': cost_per_successful_request,
        'adjusted_requests_per_week': adjusted_requests_per_week
    }

def calculate_break_even_pricing():
    """Расчет минимальной цены для клиента"""
    
    print(f"\n" + "=" * 70)
    print(f"💼 РАСЧЕТ PRICING ДЛЯ КЛИЕНТА")
    print(f"=" * 70)
    
    cost_per_request = TEST_RESULTS['total_cost_usd'] / TEST_RESULTS['successful_requests']
    
    # Разные наценки
    markups = [1.5, 2.0, 2.5, 3.0, 5.0]  # 50%, 100%, 150%, 200%, 400%
    
    print(f"📊 Себестоимость одного анализа: ${cost_per_request:.6f}")
    print(f"📊 Рекомендуемые цены для клиента (за один анализ):")
    
    for markup in markups:
        client_price = cost_per_request * markup
        profit_margin = ((markup - 1) / markup) * 100
        
        # Расчет месячного дохода
        monthly_requests = CLIENT_REQUIREMENTS['requests_per_week'] * CLIENT_REQUIREMENTS['weeks_per_month']
        monthly_revenue = monthly_requests * client_price
        monthly_costs = monthly_requests * cost_per_request * 1.2  # +20% на переделки
        monthly_profit = monthly_revenue - monthly_costs
        
        print(f"   • Наценка {(markup-1)*100:.0f}%: ${client_price:.4f} (маржа {profit_margin:.1f}%)")
        print(f"     - Месячная выручка: ${monthly_revenue:.2f}")
        print(f"     - Месячная прибыль: ${monthly_profit:.2f}")

if __name__ == "__main__":
    results = calculate_unit_economics()
    calculate_break_even_pricing()
    
    print(f"\n" + "=" * 70)
    print(f"✅ РАСЧЕТ ЗАВЕРШЕН")
    print(f"=" * 70) 