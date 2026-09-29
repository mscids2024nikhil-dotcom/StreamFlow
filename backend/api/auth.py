"""
Authentication API Endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
import sqlite3
from typing import Dict, Any
from backend.database import get_db_connection
from backend.models import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from backend.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegisterRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username or email is already taken
    existing = cursor.execute(
        "SELECT user_id FROM users WHERE username = ? OR email = ?",
        (user_data.username.strip(), user_data.email.strip().lower())
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is already registered."
        )

    hashed_pw = hash_password(user_data.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (user_data.username.strip(), hashed_pw, user_data.email.strip().lower())
        )
        conn.commit()
        user_id = cursor.lastrowid
        user_record = cursor.execute(
            "SELECT user_id, username, email, created_at FROM users WHERE user_id = ?",
            (user_id,)
        ).fetchone()
    finally:
        conn.close()

    token = create_access_token(data={"sub": user_record["user_id"], "username": user_record["username"]})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            user_id=user_record["user_id"],
            username=user_record["username"],
            email=user_record["email"],
            created_at=str(user_record["created_at"])
        )
    )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLoginRequest):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT user_id, username, password_hash, email, created_at FROM users WHERE username = ?",
        (credentials.username.strip(),)
    ).fetchone()
    conn.close()

    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(data={"sub": user["user_id"], "username": user["username"]})

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            user_id=user["user_id"],
            username=user["username"],
            email=user["email"],
            created_at=str(user["created_at"])
        )
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    return UserResponse(
        user_id=current_user["user_id"],
        username=current_user["username"],
        email=current_user["email"],
        created_at=str(current_user.get("created_at", ""))
    )
