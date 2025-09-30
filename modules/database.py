import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

# --- Database Connection Pool ---
try:
    db_pool = pooling.MySQLConnectionPool(pool_name="journal_pool", pool_size=5, host=os.getenv("MYSQL_HOST"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), database=os.getenv("MYSQL_DATABASE"))
except mysql.connector.Error as err:
    print(f"Error creating connection pool: {err}")
    db_pool = None

def get_db_connection():
    if db_pool is None: return None
    try:
        return db_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"Error getting connection from pool: {err}")
        return None

# --- User Management ---
def add_user(username, email, password_hash):
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", (username, email, password_hash))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def get_user(username):
    conn = get_db_connection()
    if not conn: return None
    cursor = None
    user = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return user

def get_user_by_email(email):
    conn = get_db_connection()
    if not conn: return None
    cursor = None
    user = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return user

def get_all_users():
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    users = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, password_hash FROM users")
        users = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return users

# --- User-Specific Data Operations ---
def save_daily_entry(user_id, date, content):
    conn = get_db_connection()
    if not conn: return None
    cursor = None
    entry_id = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO daily_entries (user_id, entry_date, content) VALUES (%s, %s, %s)", (user_id, date, content))
        entry_id = cursor.lastrowid
        conn.commit()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return entry_id

def save_entry_chunks(user_id, entry_id, entry_date, chunks):
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        chunk_data = [(user_id, entry_id, entry_date, chunk) for chunk in chunks]
        cursor.executemany("INSERT INTO entry_chunks (user_id, entry_id, entry_date, chunk_text) VALUES (%s, %s, %s, %s)", chunk_data)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def get_all_chunks(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    chunks = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, chunk_text FROM entry_chunks WHERE user_id = %s", (user_id,))
        chunks = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return chunks

def get_chunks_by_ids(user_id, chunk_ids):
    if not chunk_ids: return []
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    chunks = []
    try:
        cursor = conn.cursor(dictionary=True)
        placeholders = ','.join(['%s'] * len(chunk_ids))
        query = f"SELECT chunk_text FROM entry_chunks WHERE user_id = %s AND id IN ({placeholders})"
        cursor.execute(query, (user_id, *chunk_ids))
        chunks = [row['chunk_text'] for row in cursor.fetchall()]
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return chunks

def get_chunks_for_dates(user_id, dates):
    if not dates: return []
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    chunks = []
    try:
        cursor = conn.cursor(dictionary=True)
        placeholders = ','.join(['%s'] * len(dates))
        query = f"SELECT entry_date, chunk_text FROM entry_chunks WHERE user_id = %s AND entry_date IN ({placeholders}) ORDER BY entry_date"
        cursor.execute(query, (user_id, *dates))
        chunks = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return chunks

def get_all_entries(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    entries = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM daily_entries WHERE user_id = %s ORDER BY entry_date DESC", (user_id,))
        entries = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return entries

def get_entries_in_range(user_id, start_date, end_date):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    entries = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM daily_entries WHERE user_id = %s AND entry_date BETWEEN %s AND %s ORDER BY entry_date", (user_id, start_date, end_date))
        entries = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return entries

def get_weekly_summaries(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    summaries = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM weekly_summaries WHERE user_id = %s ORDER BY start_date DESC", (user_id,))
        summaries = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return summaries

def get_monthly_summaries(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    summaries = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM monthly_summaries WHERE user_id = %s ORDER BY start_date DESC", (user_id,))
        summaries = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return summaries

def get_weekly_summaries_in_range(user_id, start_date, end_date):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    summaries = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM weekly_summaries WHERE user_id = %s AND start_date <= %s AND end_date >= %s ORDER BY start_date"
        cursor.execute(query, (user_id, end_date, start_date))
        summaries = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return summaries

def get_monthly_summaries_in_range(user_id, start_date, end_date):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    summaries = []
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM monthly_summaries WHERE user_id = %s AND start_date <= %s AND end_date >= %s ORDER BY start_date"
        cursor.execute(query, (user_id, end_date, start_date))
        summaries = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return summaries

def save_weekly_summary(user_id, start_date, end_date, summary):
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO weekly_summaries (user_id, start_date, end_date, summary) VALUES (%s, %s, %s, %s)", (user_id, start_date, end_date, summary))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def save_monthly_summary(user_id, start_date, end_date, summary):
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO monthly_summaries (user_id, start_date, end_date, summary) VALUES (%s, %s, %s, %s)", (user_id, start_date, end_date, summary))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def save_chat_history(user_id, query, response):
    conn = get_db_connection()
    if not conn: return False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_history (user_id, query, response) VALUES (%s, %s, %s)", (user_id, query, response))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()

def get_chat_history(user_id):
    conn = get_db_connection()
    if not conn: return []
    cursor = None
    history = []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chat_history WHERE user_id = %s ORDER BY timestamp DESC", (user_id,))
        history = cursor.fetchall()
    finally:
        if conn and conn.is_connected():
            if cursor: cursor.close()
            conn.close()
    return history