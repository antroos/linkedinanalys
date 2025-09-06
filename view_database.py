#!/usr/bin/env python3
"""
View data from the image analysis results database (CLI)
"""

import sqlite3
import json

def view_analysis_by_id(analysis_id):
    """Show full analysis by ID"""
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
        print(f"📋 ANALYSIS #{result[0]}")
        print("="*80)
        print(f"🔤 Prompt: {result[1]}")
        print(f"🖼️  Image: {result[2]}")
        print(f"📊 Status: {result[3]}")
        print(f"🔢 Tokens: in={result[4]}, out={result[5]}, total={result[6]}")
        print(f"📅 Date: {result[8]}")
        print(f"\n📝 RESPONSE:")
        print("-"*80)
        print(result[7])
        print("-"*80)
    else:
        print(f"❌ Analysis #{analysis_id} not found")
    
    conn.close()


def compare_analyses():
    """Compare successful analyses"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, total_tokens, LENGTH(response_text) as response_length
        FROM analysis_results 
        WHERE status = 'SUCCESS'
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    
    print("📊 SUCCESSFUL ANALYSES COMPARISON")
    print("="*60)
    print("ID | Tokens | Response length")
    print("-"*60)
    
    for result in results:
        print(f"{result[0]:2d} | {result[1]:7d} | {result[2]:12d}")
    
    conn.close()


def search_in_responses(keyword):
    """Search by keyword in responses"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT analysis_id, status, response_text
        FROM analysis_results 
        WHERE response_text LIKE ?
        ORDER BY analysis_id
    ''', (f'%{keyword}%',))
    
    results = cursor.fetchall()
    
    print(f"🔍 SEARCH: '{keyword}'")
    print("="*60)
    
    if results:
        for result in results:
            print(f"📋 Analysis #{result[0]} ({result[1]}):")
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
        print(f"❌ Not found in responses")
    
    conn.close()


def show_menu():
    """Show CLI menu"""
    print("\n" + "="*60)
    print("🗄️  DB VIEWER")
    print("="*60)
    print("Commands:")
    print("  1-10     - Show analysis by ID")
    print("  all      - Show all analyses")
    print("  compare  - Compare successful analyses")
    print("  search   - Search by keyword")
    print("  stats    - Overall stats")
    print("  export   - Export to JSON")
    print("  help     - Show this menu")
    print("  exit     - Exit")
    print("="*60)


def show_all_analyses():
    """Show brief information about all analyses"""
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
    
    print("📋 ALL ANALYSES")
    print("="*100)
    
    for result in results:
        status_emoji = "✅" if result[1] == "SUCCESS" else "❌"
        print(f"{status_emoji} #{result[0]:2d} | {result[1]:12s} | {result[2]:4d} tokens | {result[3]}")
        print()
    
    conn.close()


def show_statistics():
    """Show detailed statistics"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    # Overall stats
    cursor.execute('SELECT * FROM test_statistics ORDER BY created_at DESC LIMIT 1')
    stats = cursor.fetchone()
    
    print("📊 OVERALL STATS")
    print("="*60)
    if stats:
        print(f"🧪 Test: {stats[1]}")
        print(f"📈 Total requests: {stats[2]}")
        print(f"✅ Successful: {stats[3]} ({stats[5]*100:.1f}%)")
        print(f"❌ Failed: {stats[4]}")
        print(f"🔢 Total tokens: {stats[8]:,}")
        print(f"💰 Total cost: ${stats[9]:.6f}")
    
    # Stats by status
    cursor.execute('''
        SELECT status, COUNT(*) as count, 
               AVG(total_tokens) as avg_tokens,
               SUM(total_tokens) as total_tokens
        FROM analysis_results 
        GROUP BY status
        ORDER BY count DESC
    ''')
    
    status_stats = cursor.fetchall()
    print(f"\n📊 BY STATUS:")
    for stat in status_stats:
        print(f"   • {stat[0]}: {stat[1]} requests | avg {stat[2]:.0f} tokens | total {stat[3]} tokens")
    
    conn.close()


def main():
    """Interactive CLI loop"""
    show_menu()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "exit":
                print("👋 Bye!")
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
                keyword = input("Keyword: ").strip()
                if keyword:
                    search_in_responses(keyword)
            elif command == "export":
                # Export to JSON
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
                print("✅ Exported to export_interactive.json")
            elif command.isdigit():
                analysis_id = int(command)
                if 1 <= analysis_id <= 10:
                    view_analysis_by_id(analysis_id)
                else:
                    print("❌ Analysis ID must be between 1 and 10")
            else:
                print("❌ Unknown command. Type 'help' for menu.")
                
        except KeyboardInterrupt:
            print("\n👋 Bye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 