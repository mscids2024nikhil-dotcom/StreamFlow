"""
Playback History Tracking API Endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict, Any
from backend.database import get_db_connection
from backend.models import HistoryUpdateRequest, HistoryResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/history", tags=["History"])

@router.post("", response_model=Dict[str, str])
def update_playback_position(
    req: HistoryUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if media exists
    media_exists = cursor.execute("SELECT media_id FROM media WHERE media_id = ?", (req.media_id,)).fetchone()
    if not media_exists:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    # Check if existing history record exists for user + media
    existing = cursor.execute(
        "SELECT history_id FROM playback_history WHERE user_id = ? AND media_id = ?",
        (current_user["user_id"], req.media_id)
    ).fetchone()

    if existing:
        cursor.execute(
            """
            UPDATE playback_history 
            SET last_position = ?, played_at = CURRENT_TIMESTAMP
            WHERE history_id = ?
            """,
            (req.last_position, existing["history_id"])
        )
    else:
        cursor.execute(
            """
            INSERT INTO playback_history (user_id, media_id, last_position)
            VALUES (?, ?, ?)
            """,
            (current_user["user_id"], req.media_id, req.last_position)
        )

    conn.commit()
    conn.close()

    return {"status": "success", "message": "Playback progress saved"}

@router.get("", response_model=List[HistoryResponse])
def get_playback_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT h.history_id, h.media_id, h.last_position, h.played_at,
               m.title, m.media_type
        FROM playback_history h
        JOIN media m ON h.media_id = m.media_id
        WHERE h.user_id = ?
        ORDER BY h.played_at DESC
        LIMIT 50;
    """, (current_user["user_id"],)).fetchall()
    conn.close()

    return [
        HistoryResponse(
            history_id=row["history_id"],
            media_id=row["media_id"],
            title=row["title"],
            media_type=row["media_type"],
            last_position=row["last_position"],
            played_at=str(row["played_at"])
        )
        for row in rows
    ]
