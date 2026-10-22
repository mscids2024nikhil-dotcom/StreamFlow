"""
Tests for Media Scanner and File Detection.
"""

import os
from backend.scanner import determine_media_type, extract_title_from_filename, scan_media_directory

def test_media_type_detection():
    assert determine_media_type(".mp3") == "audio"
    assert determine_media_type(".wav") == "audio"
    assert determine_media_type(".flac") == "audio"
    assert determine_media_type(".mp4") == "video"
    assert determine_media_type(".mkv") == "video"
    assert determine_media_type(".webm") == "video"
    assert determine_media_type(".txt") is None
    assert determine_media_type(".pdf") is None

def test_title_extraction():
    assert extract_title_from_filename("avengers_endgame.mp4") == "Avengers Endgame"
    assert extract_title_from_filename("pink_floyd_time.mp3") == "Pink Floyd Time"

def test_directory_scanning(tmp_path, setup_test_db):
    (tmp_path / "song1.mp3").write_bytes(b"dummy mp3 data")
    (tmp_path / "song2.wav").write_bytes(b"dummy wav data")
    (tmp_path / "movie.mp4").write_bytes(b"dummy mp4 data")
    (tmp_path / "clip.mkv").write_bytes(b"dummy mkv data")
    result = scan_media_directory(str(tmp_path), db_path=setup_test_db)
    assert result["status"] == "completed"
    assert result["files_found"] == 4
