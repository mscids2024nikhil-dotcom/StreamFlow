"""
Unit Tests for Database Operations and Constraints.
"""

from backend.database import get_db_connection

def test_database_initialization_and_categories(setup_test_db):
    conn = get_db_connection(setup_test_db)
    categories = conn.execute("SELECT * FROM media_categories").fetchall()
    conn.close()

    category_names = [c["category_name"] for c in categories]
    assert "Movies" in category_names
    assert "Music" in category_names
    assert len(categories) >= 5

def test_media_crud(setup_test_db):
    conn = get_db_connection(setup_test_db)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO media (title, file_path, media_type, mime_type, duration, file_size, category_id)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, ("Test Song", "/path/to/test.mp3", "audio", "audio/mpeg", 180, 5000000, 2))
    conn.commit()

    item = cursor.execute("SELECT * FROM media WHERE title = ?", ("Test Song",)).fetchone()
    assert item is not None
    assert item["media_type"] == "audio"
    assert item["duration"] == 180

    conn.close()
