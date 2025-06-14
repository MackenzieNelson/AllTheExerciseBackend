from fastapi import APIRouter, Query
from db import get_db_connection

router = APIRouter()

@router.post("/users/register")
def register_device(device_id: str = Query(..., description="Device ID of the user")):
    conn = get_db_connection()
    cursor = conn.cursor()

    #Insert Or Ignore into should ignore duplicates
    cursor.execute("""
        INSERT OR IGNORE INTO users (device_id) VALUES (?)
    """, (device_id,))

    conn.commit()
    conn.close()

    return {"message": "Device registered successfully."}
