"""
Media File Scanner & Metadata Extractor for Universal Media Streaming Platform.
"""

import os
import mimetypes
from typing import Dict, Any, List, Optional
from backend.database import get_db_connection

# Known extensions mapped to media types
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma', '.opus'}
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv', '.wmv', '.m4v'}

# Ensure proper mime types
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("video/x-matroska", ".mkv")
mimetypes.add_type("video/x-msvideo", ".avi")
mimetypes.add_type("audio/mpeg", ".mp3")
mimetypes.add_type("audio/wav", ".wav")
mimetypes.add_type("audio/ogg", ".ogg")
mimetypes.add_type("audio/flac", ".flac")

def determine_media_type(extension: str) -> Optional[str]:
    ext = extension.lower()
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return None

def extract_title_from_filename(filename: str) -> str:
    name, _ = os.path.splitext(filename)
    clean_name = name.replace("_", " ").replace(".", " ").strip()
    return clean_name.title()

def get_default_category_id(media_type: str, conn) -> Optional[int]:
    """Find default category for the given media type."""
    target_category = "Music" if media_type == "audio" else "Movies"
    row = conn.execute("SELECT category_id FROM media_categories WHERE category_name = ?", (target_category,)).fetchone()
    if row:
        return row["category_id"]
    return None

def scan_media_directory(directory_path: str, category_id: Optional[int] = None, db_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Recursively scans the provided directory path for audio and video files.
    Inserts newly discovered items into the database.
    """
    if not os.path.exists(directory_path):
        return {
            "status": "error",
            "directory": directory_path,
            "files_found": 0,
            "files_added": 0,
            "already_indexed": 0,
            "errors": [f"Directory does not exist: {directory_path}"]
        }

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    files_found = 0
    files_added = 0
    already_indexed = 0
    errors: List[str] = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            media_type = determine_media_type(ext)
            if not media_type:
                continue

            files_found += 1
            full_path = os.path.abspath(os.path.join(root, file))

            # Check if already indexed
            existing = cursor.execute("SELECT media_id FROM media WHERE file_path = ?", (full_path,)).fetchone()
            if existing:
                already_indexed += 1
                continue

            try:
                file_size = os.path.getsize(full_path)
                mime_type, _ = mimetypes.guess_type(full_path)
                if not mime_type:
                    mime_type = "video/mp4" if media_type == "video" else "audio/mpeg"

                title = extract_title_from_filename(file)
                assigned_category = category_id or get_default_category_id(media_type, conn)

                # Duration estimation fallback: approx 128kbps for audio, 1.5Mbps for video
                # If duration calculation fails, estimate based on size
                if media_type == "audio":
                    estimated_duration = max(1, int(file_size / (128 * 1024 / 8)))
                else:
                    estimated_duration = max(1, int(file_size / (1500 * 1024 / 8)))

                cursor.execute("""
                INSERT INTO media (title, file_path, media_type, mime_type, duration, file_size, category_id)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (title, full_path, media_type, mime_type, estimated_duration, file_size, assigned_category))

                files_added += 1
            except Exception as e:
                errors.append(f"Error indexing {file}: {str(e)}")

    conn.commit()
    conn.close()

    return {
        "status": "completed",
        "directory": directory_path,
        "files_found": files_found,
        "files_added": files_added,
        "already_indexed": already_indexed,
        "errors": errors
    }
