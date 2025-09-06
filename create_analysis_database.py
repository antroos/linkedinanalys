#!/usr/bin/env python3
"""
Создание базы данных для хранения результатов анализа изображений
"""

import sqlite3
import json
from datetime import datetime

# Данные из тестирования
ANALYSIS_RESULTS = [
    {
        "analysis_id": 1,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 442,
        "total_tokens": 1240,
        "response_text": """Certainly, here is the text extracted from the image:

---

**Ivan Pasichnyk 🔋 ⚡**
- Enthusiast in Smart Grids and Smart Energy. Founder & Board Member of eco-resistance non-profit. 
- Marble Climate ai 
- MIT AIx

- Private to save 
- Contact Info: 500+ connections 

---

**Analytics**
- 8,767 profile views - Discover who's viewed your profile.
- 33 post impressions - See who's discovered you via your post.
- 211 search appearances - See how often you've appeared in searches.

---

**About**
Ivan is a cofounder of EDI, a startup accelerator for clean energy hardware and smart technology, and its affiliated venture, the hardware-focused clean energy startup accelerator in Europe. I have a proven track record for creating hardware solutions for IoT. Additionally, I am passionate about energizing the world while reducing climate change. 

---

**Activity**
- 9,004 followers 
- Posts 
- Comments 
- Images

---

**Experience**

**Marble.** 
- Founder
- April 2021 - Present 2 yrs 7 mos

**eEnergy.**
- Head of Laboratory
- March 2021 - Present 2 yrs 8 mos

**UKIOT**
- Co-Founder
- March 2020 - November 2023 [3 yrs 9 mos]

---

**Education**
**The National Polytechnic Institute**
- Master of Engineering– MEng

**Open Media Accelerator powered by TechStars**

---

**Skills**
- Business Development
- Financial Planning

---

**Recommendations**

**Ivan Golan - SAI**
- [Clean]

---

**Languages**
- English - Professional working proficiency
- Polski - Elementary proficiency

---

**Organizations**

**Hack the Kitoa**
- Member - 2020 - Present

---

**Interests**

**Top Voices**
- Simon Sinek ✔️
 
**Companies**
- Anthony Watson
- Amanda Knox

**Newsletters**
- Andrew Cornelia, MBA, BA(H) XP-0
- MIT AI Impact

These are the key elements from the image, written for an audio version."""
    },
    {
        "analysis_id": 2,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 500,
        "total_tokens": 1298,
        "response_text": """Sure! Here are the extracted texts and numbers from the image:

---

Ivan Pasichnyk 3rd+ with notification badge
Tech entrepreneur. Traveler around the Europe. Former Head of ... 
The National Technical University of Ukraine 'Kyiv Polytechnic... 
156k other connections Contact info More
Open to Add profile section Showcase services Edit public pro...
Balance profile Resources
Show recruiters you're open to work- you control what is visib... 
Get started
Bring your outstanding skills and experience to service see wh...
Get started
Analytics
3753 profile views Discover who's viewed your profile and your …
33 post impressions Discover who's viewed your profile and your…
281 search appearances Discover who's viewed your profile and your ...
All highlights
About
Leading part of team Ecoisme. A home sensor is able to detect even the smallest appl...allow finding inefficient devices and replacing them with more en... Energy consumed. Is transferred into the block command application...forgetting to switch off the garage, fine tuning the usage. For the grace of c...
LinkedIn LinkedIn Facebook Facebook
* Connection
Techbanglededu.ce5 2) abet
0 up 14h
v 1 - E Resources Resources
ikS 70 Activity Create a post 
1,038 followers
Posts Comments Images 
Ivan Pasichnyk • 
46 
3w 
22 hours ago 
Shares Tech
ecohome-01.jpg 
20 
m
Eco
1 
30
Ivan Pasichnyk
Following 9 months 
Volunteer. 
linkedin.com/posts/vanpasichnyk... 
Why High-Quality 
Management of W...
Target is not ...
Understand that...
Linked
Experience ©
PILL Admmstrator Iberna Johanniter Familie
Umoja
Jan 2024 - Present1 month Jacksonville, Florida
Full-time
Ecoisme
2014 - Present 9 years 9 months 
Full-time 
Ivan at Ecoisme Add descr ... 
Founder, CEO 
Jan 2024 - Present 9 years 1 month 
To satisfy daily needs of tenants: prevent water l... 
tiVAringeort1640 on, or For t 
Resources 
Founder, CEO 
Pr
2014 - Present. 8 years 1 month
SOA
Preventing forest fires in Ukraine, course of wild horse herd increase popu... See details
nitiative. 
This could lead to the opening of a large gate."""
    },
    {
        "analysis_id": 3,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 459,
        "total_tokens": 1257,
        "response_text": """Certainly! Here is the extracted text and numbers from the image:

---

**Ivan Pasichnyk**
LinkedIn Member badge
Tech Entrepreneur | Top innovator in Europe | Former Head of B2C at Hive | Forbes Under 30
13,461 followers | 1,500+ connections

**Open to**

1. Add profile section
2. Balance profile

**Analytics**

- 738 profile views
- 23 post impressions
- 231 search appearances

**About**

Co-founder of Ecoisme, a startup backed by Telefonica, VCs and some world's top energy and utility companies. Hive is the development of the Centrica Company which is one of the UK's Top 20 Most Valuable Brands (2017). Our vision is a seamless connected home experience.

**Experience**

1. Advisor
   - Road to Product-Market-Fit (self-employed)
   - Jan 2020 - Present · 3 yrs 10 mos

2. Co-founder & CEO
   - Ecoisme
   - Jan 2014 - Dec 2019 · 6 yrs

3. Business development manager
   - PowerUp (Hardware energy startup)
   - Aug 2013 - Dec 2013 · 5 mos

**Education**

- The National Polytechnic Institute, Kyiv Polytechnic Institute
- Open Media Accelerator powered by TechStars

**Volunteering**

- Co-manager
  - Hack4Ukraine
  - Feb 2022 - Present · 1 yr 9 mos

**Skills**

- Business Development
- Financial Planning

**Recommendations**

- **Ivan Julian** - Skill: Worked with Ivan through several tech projects...
- **Alan Muzykets** - Recommend Ivan for his abilities in communication...

**Honors & Awards**

- Forbes: 30 UNDER 30 Europe, Industry
  - Aug 2016

**Languages**

- English
  - Professional working proficiency
- Polish
  - Elementary proficiency

**Organizations**

- HackLab Kyiv
  - Co-manager
  - Feb 2022 - Present · 1 yr 9 mos

**Interests**

- Simon Black
- Andrew Cornelia, MBA, BA&M, XEP-0

---

Let me know if you need further assistance!"""
    },
    {
        "analysis_id": 4,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 388,
        "total_tokens": 1186,
        "response_text": """Certainly! Here is the extracted text from the image:

---

**Ivan Pasichnyk**

- Tech entrepreneur
- Featured on 30 Under 30 Europe
- Former Head of Innovation at Clear Energy

**LinkedIn Badges**

- Verified
- Open to work
- Providing services

**Analytics**

- 783 profile views
- 33 post impressions
- 291 search appearances

**About:**

Co-founder of Ecoisme, a green tech startup that empowers home energy management through real-time monitoring. Passionate about leveraging technology to drive sustainability.

**Activity Feed:**

- Posts and Comments

**Experience:**

1. Administrator
   - PLG Ventures
   - Jan 2020 - Present, 3 years 11 months

2. Advisor

3. Founder, CEO
   - Ecoisme
   - 2013 - Present, 9 years
   - Developed smart home energy management solutions.

4. Business development manager

5. Business development

**Education:**

1. The National Polytechnic Institute
   - Bachelor of Science in Engineering

2. John Smith
   - North America

**Skills:**

- Business Development
- Financial Planning

**Recommendations:**

- Ivan Iulian
  - Senior Manager
  - John Smith

- Olga Ivanov
  - Manager
  - North American Corporation

**Languages:**

- English
  - Professional working proficiency
- Polish
  - Intermediate working proficiency

**Organizations:**

- Hack-a-Nest
  - Founder

**Interests:**

1. People
2. Companies
3. Groups
4. Newsletters
5. Schools

**Other Details:**

- Contact and Interests available
- Future 500 Forbes 30UNDER30 Europe, Industry
- Work for Patron Jan 2020 - Jan 2023

---

Let me know if you need any more details!"""
    },
    {
        "analysis_id": 5,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "FAILED_POLICY",
        "prompt_tokens": 798,
        "completion_tokens": 34,
        "total_tokens": 832,
        "response_text": "I'm unable to extract or read text from images or documents for privacy and security reasons. However, if you have any specific questions about the content, feel free to ask!"
    },
    {
        "analysis_id": 6,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 353,
        "total_tokens": 1151,
        "response_text": """Sure, here's a list of the text and numbers extracted from the image:

---

**Name:**
Ivan Pasichnyk

**Headline:**
CEO at Ecoisme | Forbes 30 under 30 Europe | Former head of NAC at YEA Ukraine

**Company:**
Ecoisme

**Location:**
Kraków, Małopolskie, Poland

**Connections:**
500+ connections

**Contact info:**
LinkedIn

**Analytics:**
721 profile views
33 post impressions
231 search appearances

**About:**
Founder and CEO of Ecoisme. Passionate about innovative technology for energy management and building solutions for the future.

**Activity:**
1,814 followers

**Experience:**
- CEO at Ecoisme
- Advisor at Accacia
- Co-Founder, CEO at Ecoisme (2012 - Present)
- Business development manager at Reloading (Jan 2015 - Aug 2015)

**Education:**
- Kyiv National Polytechnic Institute
- Open Media Accelerator powered by TechStars

**Skills:**
- Business Development
- Financial Planning

**Recommendations:**
- Ivan did an amazing job.
- Ivan is an effective manager.

**Languages:**
- English: Professional working proficiency
- Polish: Elementary proficiency

**Organizations:**
- Hack4climate

**Interests:**
- Top Voices
- Companies
- Groups

**Interests Individuals:**
- Simon Stank, Founder at Calliome (Calgary, AB)
- Andrew Cornellius, MBA, BBA/M, XEP-O, Duke Energy

**Honors & Awards:**
Forbes: 30UNDER30 (energy, industry)

---

This should cover the main text and numbers within the image."""
    },
    {
        "analysis_id": 7,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "HTTP_ERROR",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "response_text": "HTTP 400 Bad Request - nginx error"
    },
    {
        "analysis_id": 8,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 500,
        "total_tokens": 1298,
        "response_text": """Sure, here's the extracted text:

---

**Ivan Pasicznyk**
1750 followers
83 article followers

**Web3Advisor**
Former Co-founder at Ecoisme, Former Head of R&D at Virtual Broker
Education: The National Polytechnic Institute, Ignite Media Accelerator
Milwaukee, Wisconsin, United States
Certified Leader

Connections: 500+
Contact Info

**Tools**

- Open to
  1. Add profile section
  2. Balance profile
  3. Resources
  
- Analytics
  1. 1750 profile views: Discover who's viewed your profile.
  2. 33 post impressions: See how your recent post performed.
  3. 231 search appearances: See how often you appear in search.
  
- About
  *As a Founder and CEO of Ecoisme, Ivan was accountable for setting up the new technology architecture and the feature adaptation process for the UK's leading home automation system.*

**Activity**
1750 followers

1. Ivan Pasicznyk shared a post:
   Why High-Quality Essay Writing Services...
   February 25, 2023

2. Ivan Pasicznyk  commented:
   Popular AI tools: ChatGPT...
   February 25, 2023

**Experience**

- Administrator
  *Public Organization for Families*
  Oct 2019 - Present
  3 yrs 11 mos

- Advisor
  *LinkedIn*

- Founder, CEO
  *Ecoisme*
  Apr 2015 - Aug 2019
  4 yrs 5 mos

- Business development manager
  *Virtual Broker*
  Jul 2014 - Mar 2015
  9 mos

**Work Experience**
1. Administrator at Public Organization for Families
 
2. Advisor at LinkedIn
 
3. Founder, CEO at Ecoisme

4. Business development manager at Virtual Broker

**Education**
1. The National Polytechnic Institute
   Bachelor's degree
   Jun 2006 - May 2010

2. Ignite Media Accelerator powered by TechStars

**Volunteering**

- Co-coordinator
  *Hack4Ukraine*

**Skills**
- Business Development
- Financial Planning

**Recommendations**
- Deven Ishan
  *Ivan is an excellent business manager and developer...*

- Adam Hughes
  *Ivan's ability to strategize project development and lead teams to achieve goals was a part of our success...*

**Honors"""
    },
    {
        "analysis_id": 9,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 500,
        "total_tokens": 1298,
        "response_text": """Certainly! Here's the extracted text and numbers from the image:

---

**Ivan Pasichnyk**

**Open to** Add profile section Balance profile Resources

**About**
"CEO and Founder at Ecoisme, an innovative company that offers home energy monitoring solutions. I'm passionate about renewable energy, sustainability, and green technologies. With extensive international experience and numerous awards under my belt, I strive to help people use energy more efficiently and sustainably."

**Activity**
1,455 followers
Posts Comments Images

**Experience**
1. **Advisor**
   Tempest (Energy & Environment)
   Aug 2022 – Present 1 yr 3 mos

2. **Founder, CEO**
   Aug 2013 – Present 9 yrs 11 mos
   Ecoisme
   "...aims to create a full system of smart home control and help households save up to 15% on their energy consumption. Recognized by Red Dot, EDF, E.ON, and EDF..."

3. **Business development manager**
   2011 – 2013 2 yrs
   Magnat Group
   "...responsible for business strategies of company..."

**Education**
1. **Kyiv National Polytechnic Institute, Kyiv Polytechnic Institute**
   Bachelor's degree, Electrical Engineering
   2006 – 2012

2. **Open Media Accelerator powered by TechStars**

**Skills**
- Business Development
- Financial Planning
  (show all 20 skills)

**Languages**
- English: Professional working proficiency
- Polish: Elementary proficiency

**Organizations**
- **HackLab Kyiv**
   Founder
  "...Founder and mentor at HackLab Kyiv, a community dedicated to brainstorming, mentoring, and guiding young people interested in technology and engineering..."

**Recommendations**
1. **Ivan Galian - Sii**

   "...worked as project leader on a project for HP..."

2. **Julia Kowalski – Managing Partner at..**

   "...Julia's skills in both leadership and management are of the highest standard. Her capacity to transform insights into strategic..."

**Interests**
- Top Voices
- Companies
- Groups
- Newsletters
- Schools

**Simon Stack**
   Writer and producer at Film and TV industry
   "Director, Filmmaker, Partner" (student)

**Andrew Greenbloom, MBA, BBAM, XEP-G**
   Energy, Security, Smart Cities, Climate tech
   Managing Director
   "Derby Energy, Demeter Attica, Douglas &"""
    },
    {
        "analysis_id": 10,
        "prompt_text": "I am creating an audio version of this image for someone who cannot see it. Please extract and list all the text and numbers.",
        "image_file": "screenshot_2025-07-15T13-58-11-498Z.jpg",
        "status": "SUCCESS",
        "prompt_tokens": 798,
        "completion_tokens": 500,
        "total_tokens": 1298,
        "response_text": """Sure, here is the extracted text and numbers from the image:

---

**Ivan Pasichnyk**
Gold creator mode badge   
Tech entrepreneur in EU and US. Creator: WE/IuM2  Multifamily office. Acceleration of scaling.   
KPI: Architect. Elevation: 6th startup.  
Head of Research & Startups Ecosystem & CTO/COO   
IAS: Data analytic & design   
Chief EX Officer   
OpendID.   
***add profile section**   
balanced profile  
resource  
[logo] 

**Analytics**
7   266 profile views  
discover who's viewed your profile  
[View All Private mode] 
23 post impressions discover who's interested in your org posts  
2,611  search appearances  
increase your search visibility  
[View all analytics]

**Activity**  
703 followers  
Create a post  

**Ivan Pasichnyk**
14.5K followers  
23h • Edited  \+ Follow  

**Experience**  
Administrator   
IAS: Blockchain tech for banks 
Nov 2017 - Present  \|   6 yrs 

Advisor   
• 2 yrs 

Founder, CEO   
Ecoisme  
Jul 2013 - Aug 2017 \| 4 yrs 2 mos  

***add profile section**  
balanced profile  
[logo] 

**Recommendations**
[edit pending] 
Dean  
Founder at AI.   
I worked with Ivan as a manager and directly.  
During that period he set up and designed a supply chain working on complex strategies and helped implement improbable processes. He has a very extensive understanding and complex foresight when he analyses topics and holds fair ground in multiple.  
Overall I would say his skills are in drawing 

Hewitt, Naddila ( managed director )   
Founder
  
**Education**  
KPI: National Polytechnic Institute:  
Kiev. Polytechnic Institute  
Dec 2008 - Jan 2012  

Open MAH Accelerator powered by TechStars  

**Skills**
Business Development  
Financial Planning  

**Languages**
English
Professional working proficiency

Polish
Elementary proficiency

**Organizations**
HackUkraine
Hack club launched in Ukraine in 2014 empowers  
hackathons 
[logo] HackBelieve

**Interests**
Top Voices  
Companies  
Groups  
Schools  

Simon Sinek   
8,156,096 followers  

Andrew Comteeb  
Trading, Strategy, Former Alumni, Director. 4th Architect: ex Designer: B2B: FinTech"""
    }
]

def create_database():
    """Создает базу данных и таблицы"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    # Создаем таблицу для результатов анализа
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            prompt_text TEXT NOT NULL,
            image_file TEXT NOT NULL,
            status TEXT NOT NULL,
            prompt_tokens INTEGER,
            completion_tokens INTEGER,
            total_tokens INTEGER,
            response_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Создаем таблицу для общей статистики
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_name TEXT NOT NULL,
            total_requests INTEGER,
            successful_requests INTEGER,
            failed_requests INTEGER,
            success_rate REAL,
            total_prompt_tokens INTEGER,
            total_completion_tokens INTEGER,
            total_tokens INTEGER,
            total_cost_usd REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных создана успешно!")

def insert_analysis_data():
    """Вставляет данные анализа в базу"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    # Очищаем таблицу перед вставкой новых данных
    cursor.execute('DELETE FROM analysis_results')
    
    # Вставляем данные анализа
    for result in ANALYSIS_RESULTS:
        cursor.execute('''
            INSERT INTO analysis_results 
            (analysis_id, prompt_text, image_file, status, prompt_tokens, completion_tokens, total_tokens, response_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result['analysis_id'],
            result['prompt_text'],
            result['image_file'],
            result['status'],
            result['prompt_tokens'],
            result['completion_tokens'],
            result['total_tokens'],
            result['response_text']
        ))
    
    # Вставляем общую статистику теста
    cursor.execute('DELETE FROM test_statistics')
    cursor.execute('''
        INSERT INTO test_statistics 
        (test_name, total_requests, successful_requests, failed_requests, success_rate, 
         total_prompt_tokens, total_completion_tokens, total_tokens, total_cost_usd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "OpenAI GPT-4o Vision Test - Consistency Check",
        10,  # total_requests
        9,   # successful_requests
        1,   # failed_requests
        0.9, # success_rate
        7182,  # total_prompt_tokens
        3676,  # total_completion_tokens
        10858, # total_tokens
        0.054715  # total_cost_usd
    ))
    
    conn.commit()
    conn.close()
    print("✅ Данные анализа добавлены в базу!")

def query_database():
    """Выполняет запросы к базе данных для демонстрации"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("📊 СТАТИСТИКА ИЗ БАЗЫ ДАННЫХ")
    print("="*80)
    
    # Общая статистика
    cursor.execute('SELECT * FROM test_statistics ORDER BY created_at DESC LIMIT 1')
    stats = cursor.fetchone()
    if stats:
        print(f"🧪 Тест: {stats[1]}")
        print(f"📈 Всего запросов: {stats[2]}")
        print(f"✅ Успешных: {stats[3]}")
        print(f"❌ Неудачных: {stats[4]}")
        print(f"📊 Процент успеха: {stats[5]*100:.1f}%")
        print(f"💰 Общая стоимость: ${stats[9]:.6f}")
    
    # Статус каждого анализа
    print(f"\n📋 РЕЗУЛЬТАТЫ ПО АНАЛИЗАМ:")
    cursor.execute('''
        SELECT analysis_id, status, total_tokens, 
               CASE WHEN LENGTH(response_text) > 100 
                    THEN SUBSTR(response_text, 1, 100) || '...' 
                    ELSE response_text 
               END as short_response
        FROM analysis_results 
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    for result in results:
        status_emoji = "✅" if result[1] == "SUCCESS" else "❌"
        print(f"   {status_emoji} Анализ #{result[0]}: {result[1]} | {result[2]} токенов")
        print(f"      Ответ: {result[3]}")
        print()
    
    # Анализ по токенам
    cursor.execute('''
        SELECT 
            AVG(total_tokens) as avg_tokens,
            MIN(total_tokens) as min_tokens,
            MAX(total_tokens) as max_tokens,
            SUM(total_tokens) as total_tokens
        FROM analysis_results 
        WHERE status = 'SUCCESS'
    ''')
    
    token_stats = cursor.fetchone()
    if token_stats:
        print(f"🔢 СТАТИСТИКА ПО ТОКЕНАМ (только успешные):")
        print(f"   • Средние токены: {token_stats[0]:.1f}")
        print(f"   • Минимум токенов: {token_stats[1]}")
        print(f"   • Максимум токенов: {token_stats[2]}")
        print(f"   • Всего токенов: {token_stats[3]}")
    
    # Анализ по статусам
    cursor.execute('''
        SELECT status, COUNT(*) as count, 
               AVG(total_tokens) as avg_tokens
        FROM analysis_results 
        GROUP BY status
        ORDER BY count DESC
    ''')
    
    status_stats = cursor.fetchall()
    print(f"\n📊 СТАТИСТИКА ПО СТАТУСАМ:")
    for stat in status_stats:
        print(f"   • {stat[0]}: {stat[1]} запросов (сред. {stat[2]:.1f} токенов)")
    
    conn.close()

def export_to_json():
    """Экспортирует данные в JSON файл"""
    conn = sqlite3.connect('image_analysis_results.db')
    cursor = conn.cursor()
    
    # Получаем все данные
    cursor.execute('''
        SELECT analysis_id, prompt_text, image_file, status, 
               prompt_tokens, completion_tokens, total_tokens, 
               response_text, created_at
        FROM analysis_results 
        ORDER BY analysis_id
    ''')
    
    results = cursor.fetchall()
    
    # Преобразуем в список словарей
    export_data = []
    for result in results:
        export_data.append({
            "analysis_id": result[0],
            "prompt_text": result[1],
            "image_file": result[2],
            "status": result[3],
            "prompt_tokens": result[4],
            "completion_tokens": result[5],
            "total_tokens": result[6],
            "response_text": result[7],
            "created_at": result[8]
        })
    
    # Сохраняем в JSON
    with open('analysis_results_export.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    conn.close()
    print("✅ Данные экспортированы в analysis_results_export.json")

if __name__ == "__main__":
    print("🗄️  СОЗДАНИЕ БАЗЫ ДАННЫХ РЕЗУЛЬТАТОВ АНАЛИЗА")
    print("="*60)
    
    # Создаем базу данных
    create_database()
    
    # Заполняем данными
    insert_analysis_data()
    
    # Показываем статистику
    query_database()
    
    # Экспортируем в JSON
    export_to_json()
    
    print("\n" + "="*60)
    print("✅ ГОТОВО! База данных создана и заполнена")
    print("="*60)
    print("📁 Файлы:")
    print("   • image_analysis_results.db - SQLite база данных")
    print("   • analysis_results_export.json - JSON экспорт")
    print("\n💡 Для просмотра базы можешь использовать любой SQLite браузер")
    print("   или подключиться через Python/SQL запросы") 