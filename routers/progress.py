from fastapi import APIRouter, HTTPException, Query
from db import get_db_connection
from datetime import date
import logging
from routers.users import get_or_create_user

router = APIRouter()

# Update exercise progress (weight and completed status)
@router.post("/exercises/{exercise_id}/progress")
def update_exercise_progress(exercise_id: int, device_id: str, weight_used: str = "", completed: bool = False):
    user_id = get_or_create_user(device_id)

    today = date.today().isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO exercise_progress (user_id, exercise_id, date, weight_used, completed)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id, exercise_id, date) DO UPDATE SET
            weight_used=excluded.weight_used,
            completed=excluded.completed
    """
    , (user_id, exercise_id, today, weight_used, completed))
    
    conn.commit()
    conn.close()
    return {"status": "updated"}

# Mark day as complete/incomplete
@router.post("/days/{day_id}/progress")
def update_day_progress(day_id: int, device_id: str, completed: bool = False):
    user_id = get_or_create_user(device_id)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO day_progress (user_id, day_id, completed)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, day_id) DO UPDATE SET
            completed=excluded.completed
    """, (user_id, day_id, completed))

    conn.commit()
    conn.close()
    return {"status": "updated"}

# Same pattern for weeks
@router.post("/weeks/{week_id}/progress")
def update_week_progress(week_id: int, device_id: str, completed: bool = False):
    user_id = get_or_create_user(device_id)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO week_progress (user_id, week_id, completed)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, week_id) DO UPDATE SET
            completed=excluded.completed
    """, (user_id, week_id, completed))

    conn.commit()
    conn.close()
    return {"status": "updated"}

# Same pattern for programs
@router.post("/programs/{program_id}/progress")
def update_program_progress(program_id: int, device_id: str, completed: bool = False):
    user_id = get_or_create_user(device_id)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO program_progress (user_id, program_id, completed)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, program_id) DO UPDATE SET
            completed=excluded.completed
    """, (user_id, program_id, completed))

    conn.commit()
    conn.close()
    return {"status": "updated"}
