#!/usr/bin/env python3
"""
Commercial Proposal Calculator for Image Analysis Service
Клиент: обработка 5000 изображений в неделю + сравнение места работы
"""

def calculate_service_costs():
    # Базовые параметры
    images_per_week = 5000
    weeks_per_month = 4.33  # среднее количество недель в месяце
    images_per_month = images_per_week * weeks_per_month
    weeks_per_year = 52
    images_per_year = images_per_week * weeks_per_year
    
    print("=" * 80)
    print("КОММЕРЧЕСКОЕ ПРЕДЛОЖЕНИЕ - АНАЛИЗ ИЗОБРАЖЕНИЙ С ОТСЛЕЖИВАНИЕМ КАРЬЕРЫ")
    print("=" * 80)
    print(f"Объем обработки: {images_per_week:,} изображений в неделю")
    print(f"Месячный объем: {images_per_month:,.0f} изображений")
    print(f"Годовой объем: {images_per_year:,} изображений")
    print()
    
    # Стоимости из предыдущих расчетов
    ocr_cost_per_request = 0.006079  # стоимость извлечения текста из изображения
    job_analysis_cost_per_request = 0.002484  # стоимость анализа места работы
    
    # Успешность запросов
    success_rate = 0.90  # 90% успешных запросов
    retry_rate = 0.20  # 20% повторных попыток
    
    # Расчет с учетом повторных попыток
    effective_ocr_requests = images_per_week * (1 + retry_rate * (1 - success_rate))
    
    # Каждое изображение анализируется на предмет извлечения текста
    weekly_ocr_cost = effective_ocr_requests * ocr_cost_per_request
    monthly_ocr_cost = weekly_ocr_cost * weeks_per_month
    yearly_ocr_cost = weekly_ocr_cost * weeks_per_year
    
    # Анализ места работы - только для успешно обработанных изображений
    successful_analyses_per_week = images_per_week * success_rate
    weekly_job_analysis_cost = successful_analyses_per_week * job_analysis_cost_per_request
    monthly_job_analysis_cost = weekly_job_analysis_cost * weeks_per_month
    yearly_job_analysis_cost = weekly_job_analysis_cost * weeks_per_year
    
    # Отслеживание новых постов - та же стоимость что и анализ места работы
    post_tracking_cost_per_request = job_analysis_cost_per_request  # $0.002484
    weekly_post_tracking_cost = successful_analyses_per_week * post_tracking_cost_per_request
    monthly_post_tracking_cost = weekly_post_tracking_cost * weeks_per_month
    yearly_post_tracking_cost = weekly_post_tracking_cost * weeks_per_year
    
    # Общие расходы
    weekly_total_cost = weekly_ocr_cost + weekly_job_analysis_cost + weekly_post_tracking_cost
    monthly_total_cost = monthly_ocr_cost + monthly_job_analysis_cost + monthly_post_tracking_cost
    yearly_total_cost = yearly_ocr_cost + yearly_job_analysis_cost + yearly_post_tracking_cost
    
    print("ДЕТАЛИЗАЦИЯ РАСХОДОВ:")
    print("-" * 50)
    print(f"1. Извлечение текста из изображений (OCR):")
    print(f"   • Стоимость за запрос: ${ocr_cost_per_request:.6f}")
    print(f"   • Запросов в неделю (с повторами): {effective_ocr_requests:,.0f}")
    print(f"   • Еженедельно: ${weekly_ocr_cost:.2f}")
    print(f"   • Ежемесячно: ${monthly_ocr_cost:.2f}")
    print(f"   • Ежегодно: ${yearly_ocr_cost:.2f}")
    print()
    
    print(f"2. Анализ места работы:")
    print(f"   • Стоимость за анализ: ${job_analysis_cost_per_request:.6f}")
    print(f"   • Успешных анализов в неделю: {successful_analyses_per_week:,.0f}")
    print(f"   • Еженедельно: ${weekly_job_analysis_cost:.2f}")
    print(f"   • Ежемесячно: ${monthly_job_analysis_cost:.2f}")
    print(f"   • Ежегодно: ${yearly_job_analysis_cost:.2f}")
    print()
    
    print(f"3. Отслеживание новых постов:")
    print(f"   • Стоимость за анализ: ${post_tracking_cost_per_request:.6f}")
    print(f"   • Успешных анализов в неделю: {successful_analyses_per_week:,.0f}")
    print(f"   • Еженедельно: ${weekly_post_tracking_cost:.2f}")
    print(f"   • Ежемесячно: ${monthly_post_tracking_cost:.2f}")
    print(f"   • Ежегодно: ${yearly_post_tracking_cost:.2f}")
    print()
    
    print("ИТОГОВАЯ СТОИМОСТЬ СЕРВИСА:")
    print("-" * 50)
    print(f"• Еженедельно: ${weekly_total_cost:.2f}")
    print(f"• Ежемесячно: ${monthly_total_cost:.2f}")
    print(f"• Ежегодно: ${yearly_total_cost:.2f}")
    print()
    
    # Различные модели ценообразования
    print("ВАРИАНТЫ КОММЕРЧЕСКИХ ПРЕДЛОЖЕНИЙ:")
    print("=" * 50)
    
    # Вариант 1: Прямая наценка
    markup_1 = 2.5  # 150% наценка
    client_monthly_1 = monthly_total_cost * markup_1
    client_yearly_1 = yearly_total_cost * markup_1
    monthly_profit_1 = client_monthly_1 - monthly_total_cost
    
    print(f"ВАРИАНТ 1 - Стандартный пакет (наценка {(markup_1-1)*100:.0f}%):")
    print(f"   • Ежемесячная стоимость для клиента: ${client_monthly_1:.2f}")
    print(f"   • Годовая стоимость: ${client_yearly_1:.2f}")
    print(f"   • Месячная прибыль: ${monthly_profit_1:.2f}")
    print(f"   • Стоимость за изображение: ${client_monthly_1/images_per_month:.4f}")
    print()
    
    # Вариант 2: Премиум с дополнительными услугами
    markup_2 = 3.0  # 200% наценка + дополнительные услуги
    client_monthly_2 = monthly_total_cost * markup_2
    client_yearly_2 = yearly_total_cost * markup_2
    monthly_profit_2 = client_monthly_2 - monthly_total_cost
    
    print(f"ВАРИАНТ 2 - Премиум пакет (наценка {(markup_2-1)*100:.0f}%):")
    print(f"   • Ежемесячная стоимость для клиента: ${client_monthly_2:.2f}")
    print(f"   • Годовая стоимость: ${client_yearly_2:.2f}")
    print(f"   • Месячная прибыль: ${monthly_profit_2:.2f}")
    print(f"   • Стоимость за изображение: ${client_monthly_2/images_per_month:.4f}")
    print(f"   • Включает: приоритетную поддержку, детальную аналитику, API доступ")
    print()
    
    # Вариант 3: Объемная скидка
    markup_3 = 2.0  # 100% наценка при больших объемах
    client_monthly_3 = monthly_total_cost * markup_3
    client_yearly_3 = yearly_total_cost * markup_3
    monthly_profit_3 = client_monthly_3 - monthly_total_cost
    
    print(f"ВАРИАНТ 3 - Корпоративный пакет (наценка {(markup_3-1)*100:.0f}%):")
    print(f"   • Ежемесячная стоимость для клиента: ${client_monthly_3:.2f}")
    print(f"   • Годовая стоимость: ${client_yearly_3:.2f}")
    print(f"   • Месячная прибыль: ${monthly_profit_3:.2f}")
    print(f"   • Стоимость за изображение: ${client_monthly_3/images_per_month:.4f}")
    print(f"   • При годовой оплате: скидка 10%")
    print()
    
    # Расчет годовой скидки для варианта 3
    yearly_discount = 0.10
    client_yearly_3_discounted = client_yearly_3 * (1 - yearly_discount)
    yearly_savings = client_yearly_3 - client_yearly_3_discounted
    
    print(f"ВАРИАНТ 3 с годовой оплатой:")
    print(f"   • Годовая стоимость со скидкой: ${client_yearly_3_discounted:.2f}")
    print(f"   • Экономия клиента: ${yearly_savings:.2f}")
    print()
    
    # Технические характеристики
    print("ТЕХНИЧЕСКИЕ ХАРАКТЕРИСТИКИ СЕРВИСА:")
    print("-" * 50)
    print(f"• Точность извлечения текста: {success_rate*100:.0f}%")
    print(f"• Время обработки одного изображения: 3-7 секунд")
    print(f"• Поддерживаемые форматы: JPG, PNG, PDF")
    print(f"• API доступ: REST API с JSON ответами")
    print(f"• Максимальный размер изображения: 20MB")
    print(f"• Отслеживание изменений карьеры: автоматическое")
    print(f"• История анализов: полная база данных")
    print()
    
    # Преимущества автоматизации
    print("ПРЕИМУЩЕСТВА АВТОМАТИЗАЦИИ:")
    print("-" * 50)
    print("• Обработка больших объемов данных 24/7")
    print("• Стандартизированный процесс извлечения информации")
    print("• Автоматическое отслеживание изменений")
    print("• Полная история анализов в базе данных")
    print("• API интеграция для бесшовной работы")
    print("• Масштабируемость под любые объемы")
    print()
    print("РЕКОМЕНДАЦИЯ:")
    print("-" * 50)
    print(f"Для объема {images_per_week:,} изображений в неделю рекомендуем")
    print(f"Корпоративный пакет с годовой оплатой:")
    print(f"• ${client_yearly_3_discounted/12:.2f} в месяц")
    print(f"• Экономия ${yearly_savings:.2f} в год")
    print(f"• Полная автоматизация процесса")
    print(f"• Отслеживание карьерных изменений и новых постов")

if __name__ == "__main__":
    calculate_service_costs() 