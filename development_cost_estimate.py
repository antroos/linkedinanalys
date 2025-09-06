#!/usr/bin/env python3
"""
Калькулятор стоимости коммерческой разработки сервиса анализа изображений
Украинская компания -> Западные заказчики
"""

def calculate_development_costs():
    print("=" * 80)
    print("ОЦЕНКА СТОИМОСТИ КОММЕРЧЕСКОЙ РАЗРАБОТКИ")
    print("Сервис анализа изображений с AI для западных заказчиков")
    print("=" * 80)
    print()
    
    # Ставки для украинских разработчиков (USD/час)
    rates = {
        "Senior Full-Stack Developer": 35,  # Python + React
        "Senior Backend Developer": 32,     # Python/FastAPI
        "Frontend Developer": 28,           # React/TypeScript
        "DevOps Engineer": 38,              # AWS/Docker/K8s
        "AI/ML Engineer": 40,               # OpenAI API integration
        "QA Engineer": 25,                  # Testing
        "UI/UX Designer": 30,               # Design
        "Project Manager": 35,              # Management
        "Tech Lead": 45,                    # Architecture
    }
    
    print("КОМАНДА И СТАВКИ (USD/час):")
    print("-" * 50)
    for role, rate in rates.items():
        print(f"• {role:<25} ${rate}/час")
    print()
    
    # Фазы разработки и временные затраты
    phases = {
        "Фаза 1: Анализ и планирование": {
            "Tech Lead": 40,
            "Project Manager": 60,
            "UI/UX Designer": 40,
            "Senior Backend Developer": 20,
        },
        "Фаза 2: MVP Backend": {
            "Senior Backend Developer": 120,
            "AI/ML Engineer": 80,
            "DevOps Engineer": 60,
            "QA Engineer": 40,
        },
        "Фаза 3: Frontend Dashboard": {
            "Frontend Developer": 100,
            "UI/UX Designer": 60,
            "Senior Backend Developer": 20,
            "QA Engineer": 30,
        },
        "Фаза 4: API интеграция": {
            "Senior Full-Stack Developer": 80,
            "DevOps Engineer": 40,
            "QA Engineer": 40,
            "AI/ML Engineer": 30,
        },
        "Фаза 5: База данных и аналитика": {
            "Senior Backend Developer": 60,
            "Senior Full-Stack Developer": 40,
            "QA Engineer": 20,
        },
        "Фаза 6: Тестирование и деплой": {
            "QA Engineer": 80,
            "DevOps Engineer": 60,
            "Senior Backend Developer": 40,
            "Tech Lead": 20,
        },
        "Фаза 7: Документация и обучение": {
            "Tech Lead": 30,
            "Project Manager": 40,
            "Senior Backend Developer": 20,
        }
    }
    
    total_cost = 0
    total_hours = 0
    
    print("ДЕТАЛИЗАЦИЯ ПО ФАЗАМ:")
    print("=" * 50)
    
    for phase_name, phase_work in phases.items():
        phase_cost = 0
        phase_hours = 0
        
        print(f"\n{phase_name}:")
        print("-" * 40)
        
        for role, hours in phase_work.items():
            cost = hours * rates[role]
            phase_cost += cost
            phase_hours += hours
            print(f"  {role:<25} {hours:>3}ч × ${rates[role]:>2} = ${cost:>5}")
        
        print(f"  {'ИТОГО:':<25} {phase_hours:>3}ч     ${phase_cost:>5}")
        total_cost += phase_cost
        total_hours += phase_hours
    
    print("\n" + "=" * 50)
    print(f"ОБЩАЯ СТОИМОСТЬ РАЗРАБОТКИ: ${total_cost:,}")
    print(f"ОБЩЕЕ ВРЕМЯ: {total_hours} часов ({total_hours/40:.1f} недель)")
    print("=" * 50)
    print()
    
    # Дополнительные расходы
    additional_costs = {
        "Инфраструктура AWS (3 месяца)": 3000,
        "OpenAI API лимиты (тестирование)": 2000,
        "Домен и SSL сертификаты": 300,
        "Мониторинг и логирование (DataDog)": 600,
        "Юридические услуги": 2000,
        "Буферная зона (15% от разработки)": int(total_cost * 0.15),
    }
    
    print("ДОПОЛНИТЕЛЬНЫЕ РАСХОДЫ:")
    print("-" * 50)
    additional_total = 0
    for item, cost in additional_costs.items():
        print(f"• {item:<35} ${cost:>6}")
        additional_total += cost
    
    print(f"• {'ИТОГО дополнительные:':<35} ${additional_total:>6}")
    print()
    
    # Итоговая стоимость
    grand_total = total_cost + additional_total
    
    print("ИТОГОВАЯ СТОИМОСТЬ ПРОЕКТА:")
    print("=" * 50)
    print(f"Разработка:           ${total_cost:>8,}")
    print(f"Дополнительные:       ${additional_total:>8,}")
    print(f"ОБЩАЯ СТОИМОСТЬ:      ${grand_total:>8,}")
    print("=" * 50)
    print()
    
    # Варианты ценообразования для клиента
    print("ВАРИАНТЫ ПРЕДЛОЖЕНИЯ КЛИЕНТУ:")
    print("=" * 50)
    
    # Вариант 1: Cost+ модель
    markup_1 = 1.3  # 30% наценка
    client_price_1 = grand_total * markup_1
    
    print(f"ВАРИАНТ 1 - Cost+ (30% наценка):")
    print(f"• Цена для клиента: ${client_price_1:>8,.0f}")
    print(f"• Прибыль: ${client_price_1 - grand_total:>8,.0f}")
    print()
    
    # Вариант 2: Fixed Price с риском
    markup_2 = 1.5  # 50% наценка за риски
    client_price_2 = grand_total * markup_2
    
    print(f"ВАРИАНТ 2 - Fixed Price (50% наценка):")
    print(f"• Цена для клиента: ${client_price_2:>8,.0f}")
    print(f"• Прибыль: ${client_price_2 - grand_total:>8,.0f}")
    print()
    
    # Вариант 3: Поэтапная оплата
    milestone_payments = {
        "Подписание контракта (20%)": client_price_2 * 0.20,
        "MVP готов (30%)": client_price_2 * 0.30,
        "Frontend завершен (25%)": client_price_2 * 0.25,
        "Тестирование завершено (15%)": client_price_2 * 0.15,
        "Деплой и запуск (10%)": client_price_2 * 0.10,
    }
    
    print(f"ВАРИАНТ 3 - Поэтапная оплата (${client_price_2:,.0f}):")
    for milestone, payment in milestone_payments.items():
        print(f"• {milestone:<30} ${payment:>8,.0f}")
    print()
    
    # Временные рамки
    print("ВРЕМЕННЫЕ РАМКИ:")
    print("-" * 50)
    weeks_parallel = total_hours / (6 * 40)  # 6 разработчиков работают параллельно
    weeks_sequential = total_hours / 40  # один человек
    
    print(f"• При команде из 6 человек: {weeks_parallel:.1f} недель ({weeks_parallel/4:.1f} месяца)")
    print(f"• При последовательной работе: {weeks_sequential:.1f} недель ({weeks_sequential/4:.1f} месяцев)")
    print(f"• Рекомендуемый срок: {weeks_parallel + 2:.0f} недель (с буфером)")
    print()
    
    # Риски и их стоимость
    print("РИСКИ ПРОЕКТА:")
    print("-" * 50)
    risks = {
        "Изменение требований": "15-25% от стоимости",
        "Интеграция с OpenAI": "5-10% задержка",
        "Производительность под нагрузкой": "10-20% доработок",
        "Требования безопасности": "5-15% дополнительно",
        "Масштабирование архитектуры": "10-30% переработки",
    }
    
    for risk, impact in risks.items():
        print(f"• {risk:<30} {impact}")
    print()
    
    # Техническая архитектура (для понимания сложности)
    print("ТЕХНИЧЕСКАЯ АРХИТЕКТУРА:")
    print("-" * 50)
    tech_stack = {
        "Backend": "Python, FastAPI, PostgreSQL, Redis",
        "Frontend": "React, TypeScript, Material-UI",
        "AI/ML": "OpenAI GPT-4o API, Langchain",
        "Infrastructure": "AWS ECS, RDS, S3, CloudFront",
        "Monitoring": "DataDog, Sentry, AWS CloudWatch",
        "CI/CD": "GitHub Actions, Docker",
        "Security": "Auth0, WAF, VPC, Encryption",
    }
    
    for component, tech in tech_stack.items():
        print(f"• {component:<15} {tech}")
    print()
    
    # ROI для заказчика
    monthly_revenue_potential = 462.09 * 20  # 20 клиентов как в нашем примере
    payback_months = client_price_2 / monthly_revenue_potential
    
    print("ROI ДЛЯ ЗАКАЗЧИКА:")
    print("-" * 50)
    print(f"• Потенциальный доход: ${monthly_revenue_potential:,.0f}/месяц")
    print(f"• Окупаемость: {payback_months:.1f} месяцев")
    print(f"• ROI за первый год: {(monthly_revenue_potential * 12 / client_price_2 - 1) * 100:.0f}%")
    print()
    
    print("РЕКОМЕНДАЦИЯ:")
    print("=" * 50)
    print(f"Рекомендуемая цена: ${client_price_2:,.0f} (Fixed Price)")
    print(f"Срок разработки: {weeks_parallel + 2:.0f} недель")
    print(f"Команда: 6 специалистов")
    print(f"Модель оплаты: Поэтапная (5 milestone)")

if __name__ == "__main__":
    calculate_development_costs() 