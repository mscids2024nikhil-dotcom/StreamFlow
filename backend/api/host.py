"""
Host Server Diagnostics & Directory Scanner API Endpoints.
"""

import socket
import datetime
from fastapi import APIRouter, HTTPException, status
from backend.database import get_db_connection
from backend.models import HostStatusResponse, ScanDirectoryRequest, ScanSummaryResponse
from backend.scanner import scan_media_directory

router = APIRouter(prefix="/api/host", tags=["Host Management"])

def get_local_ip() -> str:
    """Detect active local Wi-Fi or Ethernet IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@router.get("/status", response_model=HostStatusResponse)
def get_host_status():
    conn = get_db_connection()
    media_count = conn.execute("SELECT COUNT(*) as cnt FROM media").fetchone()["cnt"]
    users_count = conn.execute("SELECT COUNT(*) as cnt FROM users").fetchone()["cnt"]
    conn.close()

    hostname = socket.gethostname()
    host_ip = get_local_ip()

    return HostStatusResponse(
        status="online",
        server_time=datetime.datetime.now().isoformat(),
        hostname=hostname,
        host_ip=host_ip,
        port=8000,
        total_media_count=media_count,
        total_users_count=users_count
    )

@router.post("/scan", response_model=ScanSummaryResponse)
def trigger_directory_scan(req: ScanDirectoryRequest):
    result = scan_media_directory(
        directory_path=req.directory_path,
        category_id=req.category_id
    )
    return ScanSummaryResponse(
        status=result["status"],
        directory=result["directory"],
        files_found=result["files_found"],
        files_added=result["files_added"],
        already_indexed=result["already_indexed"],
        errors=result["errors"]
    )
