from fastapi import APIRouter
from db import get_db_connection

router = APIRouter()

def get_or_create_user(device_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE device_id = ?", (device_id,))
    row = cursor.fetchone()

    if row:
        user_id = row["id"]
    else:
        cursor.execute("INSERT INTO users (device_id) VALUES (?)", (device_id,))
        conn.commit()
        user_id = cursor.lastrowid

    conn.close()
    return user_id
