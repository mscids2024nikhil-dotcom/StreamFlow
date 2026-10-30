"""
Launcher script for Universal Media Streaming Platform.
Runs FastAPI on host 0.0.0.0 and port 8000, making it available across the local Wi-Fi network.
"""

import uvicorn
import socket
import os

def print_banner():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.3)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        local_ip = ip
    except Exception:
        local_ip = "127.0.0.1"

    print("=" * 65)
    print("      UNIVERSAL MEDIA STREAMING PLATFORM (StreamFlow)")
    print("      Software Engineering - SEA Project")
    print("      Team: Nikhil Chari, Bhiva Korkhankar, Christopher Sequeira")
    print("=" * 65)
    print(f"[*] Local Host Access:     http://localhost:8000")
    print(f"[*] Local Wi-Fi Network:   http://{local_ip}:8000")
    print(f"[*] Interactive API Docs:  http://{local_ip}:8000/docs")
    print("=" * 65)
    print("[*] Press Ctrl+C to terminate the server.\n")

if __name__ == "__main__":
    print_banner()
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
