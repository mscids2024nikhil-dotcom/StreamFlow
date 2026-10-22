"""
Tests for HTTP Byte-Range Streaming and Playback History.
"""

import os
from backend.streaming import parse_range_header
from backend.database import get_db_connection

def test_parse_range_header():
    total_size = 10000

    # Range: bytes=0-499
    start, end = parse_range_header("bytes=0-499", total_size)
    assert start == 0
    assert end == 499

    # Range: bytes=1000-
    start, end = parse_range_header("bytes=1000-", total_size)
    assert start == 1000
    assert end == 9999

    # Suffix range: bytes=-500
    start, end = parse_range_header("bytes=-500", total_size)
    assert start == 9500
    assert end == 9999

def test_stream_api_endpoint(client, setup_test_db, tmp_path):
    # Create temporary media file for stream verification
    test_file = tmp_path / "test_stream.mp4"
    test_file.write_bytes(b"0123456789" * 500)
    conn = get_db_connection(setup_test_db)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO media (title, file_path, media_type, mime_type, duration, file_size, category_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("Stream Test Clip", str(test_file), "video", "video/mp4", 30, 5000, 1))
    media_id = cursor.lastrowid
    conn.commit()
    conn.close()

    file_size = 5000

    # 1. Full stream request without Range header
    res_full = client.get(f"/api/media/{media_id}/stream")
    assert res_full.status_code == 200
    assert res_full.headers["accept-ranges"] == "bytes"
    assert int(res_full.headers["content-length"]) == file_size

    # 2. Byte Range Request (first 100 bytes)
    res_range = client.get(
        f"/api/media/{media_id}/stream",
        headers={"Range": "bytes=0-99"}
    )
    assert res_range.status_code == 206
    assert res_range.headers["accept-ranges"] == "bytes"
    assert res_range.headers["content-range"] == f"bytes 0-99/{file_size}"
    assert int(res_range.headers["content-length"]) == 100
    assert len(res_range.content) == 100

    # 3. Seeking Range Request (offset 500 onwards)
    seek_start = min(500, file_size - 1)
    res_seek = client.get(
        f"/api/media/{media_id}/stream",
        headers={"Range": f"bytes={seek_start}-"}
    )
    assert res_seek.status_code == 206
    expected_length = (file_size - 1 - seek_start) + 1
    assert int(res_seek.headers["content-length"]) == expected_length

def test_playback_history_flow(client, setup_test_db):
    # Register & get token
    auth_res = client.post("/api/auth/register", json={
        "username": "streamer",
        "email": "streamer@stream.com",
        "password": "password123"
    })
    token = auth_res.json()["access_token"]

    conn = get_db_connection(setup_test_db)
    media_item = conn.execute("SELECT * FROM media LIMIT 1").fetchone()
    conn.close()

    media_id = media_item["media_id"]

    # Save playback progress
    update_res = client.post(
        "/api/history",
        headers={"Authorization": f"Bearer {token}"},
        json={"media_id": media_id, "last_position": 45}
    )
    assert update_res.status_code == 200

    # Fetch history
    hist_res = client.get("/api/history", headers={"Authorization": f"Bearer {token}"})
    assert hist_res.status_code == 200
    history_items = hist_res.json()
    assert len(history_items) >= 1
    assert history_items[0]["media_id"] == media_id
    assert history_items[0]["last_position"] == 45
