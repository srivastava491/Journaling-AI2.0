import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def save_daily_entry(date, content):
    conn = get_db_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO daily_entries (entry_date, content) VALUES (%s, %s)", (date, content))
    conn.commit()
    cursor.close()
    conn.close()

def get_entries_in_range(start_date, end_date):
    conn = get_db_connection()
    if conn is None: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM daily_entries WHERE entry_date BETWEEN %s AND %s ORDER BY entry_date DESC", (start_date, end_date))
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return entries

def save_chat_history(query, response):
    conn = get_db_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (query, response) VALUES (%s, %s)", (query, response))
    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history():
    conn = get_db_connection()
    if conn is None: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC")
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history

def save_weekly_summary(start_date, end_date, summary):
    conn = get_db_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weekly_summaries (start_date, end_date, summary) VALUES (%s, %s, %s)", (start_date, end_date, summary))
    conn.commit()
    cursor.close()
    conn.close()

def save_monthly_summary(start_date, end_date, summary):
    conn = get_db_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO monthly_summaries (start_date, end_date, summary) VALUES (%s, %s, %s)", (start_date, end_date, summary))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_daily_entries():
    conn = get_db_connection()
    if conn is None: return []
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, content FROM daily_entries ORDER BY entry_date ASC")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return entries

def clear_chunks_table():
    conn = get_db_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entry_chunks")
    conn.commit()
    cursor.close()
    conn.close() 