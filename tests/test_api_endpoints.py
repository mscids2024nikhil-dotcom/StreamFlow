"""
Integration tests for Host Diagnostics, Categories, and Media Listing endpoints.
"""

from backend.database import get_db_connection

def test_host_status_endpoint(client):
    res = client.get("/api/host/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "host_ip" in data
    assert "port" in data
    assert data["port"] == 8000
    assert "total_media_count" in data

def test_categories_api(client):
    res = client.get("/api/categories")
    assert res.status_code == 200
    categories = res.json()
    assert len(categories) >= 5
    cat_names = [c["category_name"] for c in categories]
    assert "Movies" in cat_names

def test_media_filtering_and_pagination(client):
    # Filter audio
    res_audio = client.get("/api/media?media_type=audio")
    assert res_audio.status_code == 200
    for item in res_audio.json()["items"]:
        assert item["media_type"] == "audio"

    # Filter video
    res_video = client.get("/api/media?media_type=video")
    assert res_video.status_code == 200
    for item in res_video.json()["items"]:
        assert item["media_type"] == "video"

def test_invalid_media_stream_not_found(client):
    res = client.get("/api/media/999999/stream")
    assert res.status_code == 404
