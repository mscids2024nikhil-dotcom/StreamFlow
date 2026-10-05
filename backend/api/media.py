"""
Media and Category Management & Streaming Endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Query, Request, Header
from typing import Optional, List
from backend.database import get_db_connection
from backend.models import CategoryResponse, CategoryCreate, MediaResponse, MediaListResponse
from backend.streaming import get_media_stream_response

router = APIRouter(prefix="/api", tags=["Media"])

@router.get("/categories", response_model=List[CategoryResponse])
def list_categories():
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT c.category_id, c.category_name, c.description, COUNT(m.media_id) as media_count
        FROM media_categories c
        LEFT JOIN media m ON c.category_id = m.category_id
        GROUP BY c.category_id
        ORDER BY c.category_name ASC;
    """).fetchall()
    conn.close()

    return [
        CategoryResponse(
            category_id=row["category_id"],
            category_name=row["category_name"],
            description=row["description"],
            media_count=row["media_count"]
        )
        for row in rows
    ]

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(cat: CategoryCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO media_categories (category_name, description) VALUES (?, ?)",
            (cat.category_name.strip(), cat.description)
        )
        conn.commit()
        cat_id = cursor.lastrowid
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Category creation failed: {str(e)}")

    row = cursor.execute("SELECT * FROM media_categories WHERE category_id = ?", (cat_id,)).fetchone()
    conn.close()

    return CategoryResponse(
        category_id=row["category_id"],
        category_name=row["category_name"],
        description=row["description"],
        media_count=0
    )

@router.get("/media", response_model=MediaListResponse)
def list_media(
    category_id: Optional[int] = Query(None, description="Filter by category"),
    media_type: Optional[str] = Query(None, pattern="^(audio|video)$", description="Filter by media type"),
    search: Optional[str] = Query(None, description="Search by title"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    conn = get_db_connection()
    query = """
        SELECT m.media_id, m.title, m.file_path, m.media_type, m.mime_type, 
               m.duration, m.file_size, m.category_id, m.created_at,
               c.category_name
        FROM media m
        LEFT JOIN media_categories c ON m.category_id = c.category_id
        WHERE 1=1
    """
    params = []

    if category_id:
        query += " AND m.category_id = ?"
        params.append(category_id)

    if media_type:
        query += " AND m.media_type = ?"
        params.append(media_type)

    if search:
        query += " AND m.title LIKE ?"
        params.append(f"%{search.strip()}%")

    count_query = f"SELECT COUNT(*) as cnt FROM ({query})"
    total_count = conn.execute(count_query, params).fetchone()["cnt"]

    query += " ORDER BY m.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = conn.execute(query, params).fetchall()
    conn.close()

    items = [
        MediaResponse(
            media_id=row["media_id"],
            title=row["title"],
            file_path=row["file_path"],
            media_type=row["media_type"],
            mime_type=row["mime_type"],
            duration=row["duration"],
            file_size=row["file_size"],
            category_id=row["category_id"],
            category_name=row["category_name"],
            created_at=str(row["created_at"])
        )
        for row in rows
    ]

    return MediaListResponse(total=total_count, items=items)

@router.get("/media/{media_id}", response_model=MediaResponse)
def get_media_item(media_id: int):
    conn = get_db_connection()
    row = conn.execute("""
        SELECT m.media_id, m.title, m.file_path, m.media_type, m.mime_type, 
               m.duration, m.file_size, m.category_id, m.created_at,
               c.category_name
        FROM media m
        LEFT JOIN media_categories c ON m.category_id = c.category_id
        WHERE m.media_id = ?
    """, (media_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media item not found")

    return MediaResponse(
        media_id=row["media_id"],
        title=row["title"],
        file_path=row["file_path"],
        media_type=row["media_type"],
        mime_type=row["mime_type"],
        duration=row["duration"],
        file_size=row["file_size"],
        category_id=row["category_id"],
        category_name=row["category_name"],
        created_at=str(row["created_at"])
    )

@router.get("/media/{media_id}/stream")
def stream_media(media_id: int, request: Request, range: Optional[str] = Header(None)):
    """
    Stream media with HTTP Range byte-seeking capability (RFC 7233).
    Supports HTML5 video/audio tag streaming, seeking and scrubber controls.
    """
    conn = get_db_connection()
    row = conn.execute("SELECT file_path, mime_type FROM media WHERE media_id = ?", (media_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    range_header = range or request.headers.get("range")
    return get_media_stream_response(
        file_path=row["file_path"],
        mime_type=row["mime_type"],
        range_header=range_header
    )
