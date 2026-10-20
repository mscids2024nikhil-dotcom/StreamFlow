"""
Pytest Fixtures and Test Database Configuration.
"""

import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db, get_db_connection

TEST_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_media.db")

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

    # Initialize schema
    init_db(TEST_DB_PATH)

    # Override default DB path in database module for testing
    import backend.database as db_mod
    original_path = db_mod.DEFAULT_DB_PATH
    db_mod.DEFAULT_DB_PATH = TEST_DB_PATH

    yield TEST_DB_PATH

    db_mod.DEFAULT_DB_PATH = original_path
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
