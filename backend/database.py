"""
SQLite Database Connection and Schema Management for Universal Media Streaming Platform.
"""

import sqlite3
import os
from typing import Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media_stream.db")

def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a connection with Row factory enabled."""
    target_path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(target_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: Optional[str] = None) -> None:
    """Initialize database tables, indexes, and default categories."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Media Categories Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media_categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL UNIQUE,
        description TEXT
    );
    """)

    # 3. Media Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS media (
        media_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        file_path TEXT NOT NULL UNIQUE,
        media_type TEXT NOT NULL CHECK(media_type IN ('audio', 'video')),
        mime_type TEXT NOT NULL,
        duration INTEGER DEFAULT 0,
        file_size INTEGER NOT NULL,
        category_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES media_categories(category_id) ON DELETE SET NULL
    );
    """)

    # 4. Playback History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS playback_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        media_id INTEGER NOT NULL,
        last_position INTEGER NOT NULL DEFAULT 0,
        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (media_id) REFERENCES media(media_id) ON DELETE CASCADE
    );
    """)

    # Indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_media_category ON media(category_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_user ON playback_history(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_user_media ON playback_history(user_id, media_id);")

    # Seed initial default categories if not present
    default_categories = [
        ("Movies", "Feature films and cinema"),
        ("Music", "Audio tracks, songs, and albums"),
        ("Podcasts", "Recorded audio episodes and talk shows"),
        ("Series", "Television and episodic video shows"),
        ("Personal Clips", "Recorded home videos and audio memos")
    ]
    cursor.executemany("""
    INSERT OR IGNORE INTO media_categories (category_name, description)
    VALUES (?, ?);
    """, default_categories)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DEFAULT_DB_PATH)
