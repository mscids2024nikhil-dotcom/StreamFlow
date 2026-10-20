"""
Unit Tests for Authentication and Cryptography.
"""

import pytest
from backend.auth import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    pw = "SuperSecret123"
    hashed = hash_password(pw)
    assert hashed != pw
    assert "$" in hashed
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_generation_and_decoding():
    payload = {"sub": 42, "username": "nikhil"}
    token = create_access_token(payload, expires_delta=300)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3

    decoded = decode_access_token(token)
    assert decoded["sub"] == 42
    assert decoded["username"] == "nikhil"
    assert "exp" in decoded

def test_auth_api_flow(client):
    # Register new user
    reg_res = client.post("/api/auth/register", json={
        "username": "tester1",
        "email": "tester1@example.com",
        "password": "mypassword123"
    })
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["username"] == "tester1"

    token = reg_data["access_token"]

    # Duplicate registration must fail
    dup_res = client.post("/api/auth/register", json={
        "username": "tester1",
        "email": "another@example.com",
        "password": "mypassword123"
    })
    assert dup_res.status_code == 400

    # Login with valid credentials
    login_res = client.post("/api/auth/login", json={
        "username": "tester1",
        "password": "mypassword123"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # Login with invalid password
    bad_login = client.post("/api/auth/login", json={
        "username": "tester1",
        "password": "wrongpassword"
    })
    assert bad_login.status_code == 401

    # Protected route with token
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "tester1"

    # Protected route without token
    no_auth = client.get("/api/auth/me")
    assert no_auth.status_code == 401
