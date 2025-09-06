#!/usr/bin/env python3
"""
Просмотр данных из базы результатов анализа
"""

import sqlite3
import json

def view_analysis_by_id(analysis_id):
    """Показать полный анализ по ID"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, prompt_text, image_file, status, 
               prompt_tokens, completion_tokens, total_tokens, 
               response_text, created_at
        FROM analysis_results 
        WHERE analysis_id = ?
    ''', (analysis_id,))
    
    result = cursor.fetchone()
    if result:
        print(f"📋 АНАЛИЗ #{result[0]}")
        print("="*80)
        print(f"🔤 Промпт: {result[1]}")
        print(f"🖼️  Изображение: {result[2]}")
        print(f"📊 Статус: {result[3]}")
        print(f"🔢 Токены: вход={result[4]}, выход={result[5]}, всего={result[6]}")
        print(f"📅 Дата: {result[8]}")
        print(f"\n📝 ОТВЕТ:")
        print("-"*80)
        print(result[7])
        print("-"*80)
    else:
        print(f"❌ Анализ #{analysis_id} не найден")
    
    conn.close()

def compare_analyses():
    """Сравнить все успешные анализы"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, total_tokens, LENGTH(response_text) as response_length
        FROM analysis_results 
        WHERE status = 'SUCCESS'
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    
    print("📊 СРАВНЕНИЕ УСПЕШНЫХ АНАЛИЗОВ")
    print("="*60)
    print("ID | Токенов | Длина ответа")
    print("-"*60)
    
    for result in results:
        print(f"{result[0]:2d} | {result[1]:7d} | {result[2]:12d}")
    
    conn.close()

def search_in_responses(keyword):
    """Поиск по ключевому слову в ответах"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, status, response_text
        FROM analysis_results 
        WHERE response_text LIKE ?
        ORDER BY analysis_id
    ''', (f'%{keyword}%',))
    
    results = cursor.fetchall()
    
    print(f"🔍 ПОИСК ПО СЛОВУ: '{keyword}'")
    print("="*60)
    
    if results:
        for result in results:
            print(f"📋 Анализ #{result[0]} ({result[1]}):")
            # Показываем контекст вокруг найденного слова
            text = result[2]
            keyword_lower = keyword.lower()
            text_lower = text.lower()
            
            if keyword_lower in text_lower:
                start = max(0, text_lower.find(keyword_lower) - 50)
                end = min(len(text), text_lower.find(keyword_lower) + len(keyword) + 50)
                context = text[start:end]
                print(f"   ...{context}...")
            print()
    else:
        print(f"❌ Слово '{keyword}' не найдено в ответах")
    
    conn.close()

def show_menu():
    """Показать меню команд"""
    print("\n" + "="*60)
    print("🗄️  ПРОСМОТР БАЗЫ ДАННЫХ АНАЛИЗОВ")
    print("="*60)
    print("Команды:")
    print("  1-10     - Показать анализ по номеру")
    print("  all      - Показать все анализы")
    print("  compare  - Сравнить успешные анализы")
    print("  search   - Поиск по ключевому слову")
    print("  stats    - Общая статистика")
    print("  export   - Экспорт в JSON")
    print("  help     - Показать это меню")
    print("  exit     - Выход")
    print("="*60)

def show_all_analyses():
    """Показать краткую информацию о всех анализах"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, status, total_tokens,
               CASE WHEN LENGTH(response_text) > 80 
                    THEN SUBSTR(response_text, 1, 80) || '...' 
                    ELSE response_text 
               END as short_response
        FROM analysis_results 
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    
    print("📋 ВСЕ АНАЛИЗЫ")
    print("="*100)
    
    for result in results:
        status_emoji = "✅" if result[1] == "SUCCESS" else "❌"
        print(f"{status_emoji} #{result[0]:2d} | {result[1]:12s} | {result[2]:4d} токенов | {result[3]}")
        print()
    
    conn.close()

def show_statistics():
    """Показать подробную статистику"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    # Общая статистика
    cursor.execute('SELECT * FROM test_statistics ORDER BY created_at DESC LIMIT 1')
    stats = cursor.fetchone()
    
    print("📊 ОБЩАЯ СТАТИСТИКА")
    print("="*60)
    if stats:
        print(f"🧪 Тест: {stats[1]}")
        print(f"📈 Всего запросов: {stats[2]}")
        print(f"✅ Успешных: {stats[3]} ({stats[5]*100:.1f}%)")
        print(f"❌ Неудачных: {stats[4]}")
        print(f"🔢 Всего токенов: {stats[8]:,}")
        print(f"💰 Общая стоимость: ${stats[9]:.6f}")
        print(f"💵 Стоимость за токен: ${stats[9]/stats[8]:.8f}")
    
    # Статистика по статусам
    cursor.execute('''
        SELECT status, COUNT(*) as count, 
               AVG(total_tokens) as avg_tokens,
               SUM(total_tokens) as total_tokens
        FROM analysis_results 
        GROUP BY status
        ORDER BY count DESC
    ''')
    
    status_stats = cursor.fetchall()
    print(f"\n📊 ПО СТАТУСАМ:")
    for stat in status_stats:
        print(f"   • {stat[0]}: {stat[1]} запросов | ср.{stat[2]:.0f} токенов | всего {stat[3]} токенов")
    
    conn.close()

def main():
    """Основной интерактивный цикл"""
    show_menu()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "exit":
                print("👋 До свидания!")
                break
            elif command == "help":
                show_menu()
            elif command == "all":
                show_all_analyses()
            elif command == "compare":
                compare_analyses()
            elif command == "stats":
                show_statistics()
            elif command == "search":
                keyword = input("Введите ключевое слово: ").strip()
                if keyword:
                    search_in_responses(keyword)
            elif command == "export":
                # Экспорт в JSON
                conn = sqlite3.connect('image_analysis_results.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM analysis_results ORDER BY analysis_id')
                results = cursor.fetchall()
                
                export_data = []
                for result in results:
                    export_data.append({
                        "id": result[0],
                        "analysis_id": result[1],
                        "prompt_text": result[2],
                        "image_file": result[3],
                        "status": result[4],
                        "tokens": {"prompt": result[5], "completion": result[6], "total": result[7]},
                        "response_text": result[8],
                        "created_at": result[9]
                    })
                
                with open('export_interactive.json', 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                conn.close()
                print("✅ Экспортировано в export_interactive.json")
            elif command.isdigit():
                analysis_id = int(command)
                if 1 <= analysis_id <= 10:
                    view_analysis_by_id(analysis_id)
                else:
                    print("❌ ID анализа должен быть от 1 до 10")
            else:
                print("❌ Неизвестная команда. Введите 'help' для справки.")
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 