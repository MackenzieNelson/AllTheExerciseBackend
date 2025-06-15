from fastapi import APIRouter, Query
from db import get_db_connection
from routers.users import get_or_create_user

router = APIRouter()

@router.get("/programs")
def get_programs(device_id: str = Query(...)):
    user_id = get_or_create_user(device_id)

    conn = get_db_connection()
    cursor = conn.cursor()

    programs = cursor.execute("""
        SELECT p.id, p.name, el.title AS library_title
        FROM programs p
        LEFT JOIN exercise_library el ON p.library_id = el.id
    """).fetchall()

    result = []
    for p in programs:
        progress = cursor.execute("""
            SELECT completed
            FROM program_progress
            WHERE user_id = ? AND program_id = ?
        """, (user_id, p["id"])).fetchone()

        result.append({
            "id": p["id"],
            "name": p["name"],
            "library_title": p["library_title"],
            "completed": bool(progress["completed"]) if progress else False
        })

    conn.close()
    return result
