from fastapi import APIRouter, Query
from db import get_db_connection
from routers.users import get_or_create_user

router = APIRouter()

@router.get("/days/{day_id}/exercises")
def get_day_exercises(day_id: int, device_id: str = Query(...)):
    user_id = get_or_create_user(device_id)
    conn = get_db_connection()
    cursor = conn.cursor()

    exercises = cursor.execute("""
        SELECT id, name, reps, rpe, rest, load, warmUpSets, workingSets, notes
        FROM exercises
        WHERE day_id = ?
    """, (day_id,)).fetchall()

    result = []
    for e in exercises:
        progress = cursor.execute("""
            SELECT weight_used, completed
            FROM exercise_progress
            WHERE user_id = ? AND exercise_id = ?
            ORDER BY date DESC
            LIMIT 1
        """, (user_id, e["id"])).fetchone()

        result.append({
            "id": e["id"],
            "name": e["name"],
            "reps": e["reps"],
            "rpe": e["rpe"],
            "rest": e["rest"],
            "load": e["load"],
            "warmUpSets": e["warmUpSets"],
            "workingSets": e["workingSets"],
            "notes": e["notes"],
            "completed": bool(progress["completed"]) if progress else False,
            "weight_used": progress["weight_used"] if progress else None
        })

    conn.close()
    return result

@router.get("/exercises/{exercise_id}/substitutions")
def get_exercise_substitutions(exercise_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    substitutions = cursor.execute("""
        SELECT substitution_name
        FROM substitutions
        WHERE exercise_id = ?
    """, (exercise_id,)).fetchall()

    conn.close()
    return {
        "exercise_id": exercise_id,
        "substitutions": [s["substitution_name"] for s in substitutions]
    }
