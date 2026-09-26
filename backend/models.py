"""
Pydantic Schemas for Request & Response Data Transfer Objects (DTOs).
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ----------------- Auth Models -----------------
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=6, max_length=128)

class UserLoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# ----------------- Category Models -----------------
class CategoryCreate(BaseModel):
    category_name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    description: Optional[str] = None
    media_count: Optional[int] = 0

# ----------------- Media Models -----------------
class MediaResponse(BaseModel):
    media_id: int
    title: str
    file_path: str
    media_type: str
    mime_type: str
    duration: int
    file_size: int
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    created_at: Optional[str] = None

class MediaListResponse(BaseModel):
    total: int
    items: List[MediaResponse]

# ----------------- History Models -----------------
class HistoryUpdateRequest(BaseModel):
    media_id: int
    last_position: int = Field(..., ge=0)

class HistoryResponse(BaseModel):
    history_id: int
    media_id: int
    title: str
    media_type: str
    last_position: int
    played_at: str

# ----------------- Host Diagnostics Models -----------------
class HostStatusResponse(BaseModel):
    status: str = "online"
    server_time: str
    hostname: str
    host_ip: str
    port: int
    total_media_count: int
    total_users_count: int

class ScanDirectoryRequest(BaseModel):
    directory_path: str
    category_id: Optional[int] = None

class ScanSummaryResponse(BaseModel):
    status: str
    directory: str
    files_found: int
    files_added: int
    already_indexed: int
    errors: List[str] = []
