"""
FastAPI Main Application for Universal Media Streaming Platform.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import init_db
from backend.api.auth import router as auth_router
from backend.api.media import router as media_router
from backend.api.history import router as history_router
from backend.api.host import router as host_router

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database and tables exist
    init_db()
    yield
    # Shutdown

app = FastAPI(
    title="Universal Media Streaming Platform API",
    description="Cross-platform backend for audio/video media indexing and HTTP range streaming.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Flutter clients (Windows/Android) and Web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Accept-Ranges", "Content-Length", "Content-Type"]
)

# Include API Routers
app.include_router(auth_router)
app.include_router(media_router)
app.include_router(history_router)
app.include_router(host_router)

# Mount Static Files (Web Client)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "status": "online",
        "message": "Universal Media Streaming Platform API is running.",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
