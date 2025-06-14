import sqlite3

def get_db_connection():
    conn = sqlite3.connect("all_the_exercise.db", timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
