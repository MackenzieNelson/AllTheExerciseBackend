from fastapi import APIRouter, Query
from db import get_db_connection

router = APIRouter()

@router.get("/programs/{program_id}/days")
def get_program_days(program_id: int, device_id: str = Query(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    result = cursor.execute("""
        SELECT
            weeks.id AS week_id,
            weeks.week_number,
            days.id AS day_id,
            days.name AS day_name
        FROM weeks
        JOIN days ON days.week_id = weeks.id
        WHERE weeks.program_id = ?
        ORDER BY weeks.week_number, days.id
    """, (program_id,)).fetchall()

    weeks = {}
    for row in result:
        week_num = row["week_number"]

        # Check day progress
        progress = cursor.execute("""
            SELECT completed
            FROM day_progress
            WHERE user_id = ? AND day_id = ?
        """, (device_id, row["day_id"])).fetchone()

        if week_num not in weeks:
            weeks[week_num] = {
                "week_number": week_num,
                "week_id": row["week_id"],
                "days": []
            }

        weeks[week_num]["days"].append({
            "day_id": row["day_id"],
            "day_name": row["day_name"],
            "completed": bool(progress["completed"]) if progress else False
        })

    conn.close()
    return list(weeks.values())
