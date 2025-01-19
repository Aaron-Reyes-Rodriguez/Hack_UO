# Contains utility functions like schedule comparison.

from bs4 import BeautifulSoup
import sqlite3
from collections import defaultdict

def extract_schedule_data(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.find('table')
    schedule_data = []
    
    if table:
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if len(columns) >= 8:
                course = columns[1].get_text(strip=True)
                title = columns[2].get_text(strip=True)
                days = columns[7].get_text(strip=True)
                time = columns[8].get_text(strip=True)
                
                if time != "TBA":
                    start_time, end_time = time.split(' - ')
                else:
                    start_time, end_time = "TBA", "TBA"
                
                schedule_data.append({
                    'course': course,
                    'title': title,
                    'days': list(days),
                    'start_time': start_time,
                    'end_time': end_time
                })
    
    return schedule_data

def store_schedule_in_db(schedule_data):
    conn = sqlite3.connect('database/schedules.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT,
            title TEXT,
            day TEXT,
            start_time TEXT,
            end_time TEXT
        )
    ''')
    
    for entry in schedule_data:
        for day in entry['days']:
            cursor.execute('''
                INSERT INTO schedules (course, title, day, start_time, end_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (entry['course'], entry['title'], day, entry['start_time'], entry['end_time']))
    
    conn.commit()
    conn.close()

def fetch_schedules():
    conn = sqlite3.connect('database/schedules.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT course, title, day, start_time, end_time FROM schedules')
    rows = cursor.fetchall()
    
    conn.close()
    
    schedules = [
        {
            "course": row[0],
            "title": row[1],
            "days": [row[2]],
            "start_time": row[3],
            "end_time": row[4]
        }
        for row in rows
    ]
    
    return schedules

def convert_time_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def find_common_free_times(schedules):
    schedules_by_day = defaultdict(lambda: defaultdict(list))
    for schedule in schedules:
        for day in schedule['days']:
            schedules_by_day[day][schedule['user_id']].append(schedule)
    
    common_free_times = defaultdict(list)
    
    for day, user_schedules in schedules_by_day.items():
        free_times_by_user = {}
        for user_id, classes in user_schedules.items():
            classes.sort(key=lambda x: convert_time_to_minutes(x['start_time']))
            free_times = []
            end_of_last_class = 0
            
            for cls in classes:
                start_time = convert_time_to_minutes(cls['start_time'])
                if start_time > end_of_last_class:
                    free_times.append((end_of_last_class, start_time))
                end_of_last_class = max(end_of_last_class, convert_time_to_minutes(cls['end_time']))
            
            if end_of_last_class < 1440:
                free_times.append((end_of_last_class, 1440))
            
            free_times_by_user[user_id] = free_times
        
        common_times = set(free_times_by_user[next(iter(free_times_by_user))])
        for free_times in free_times_by_user.values():
            common_times.intersection_update(free_times)
        
        common_free_times[day] = list(common_times)
    
    return common_free_times
