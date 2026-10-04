"""
HTTP Byte-Range Streaming Engine conforming to RFC 7233.
Allows audio and video players to seek, buffer, and scrub without loading entire files into memory.
"""

import os
import re
from typing import Generator, Optional
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse

# 64 KB chunk size for smooth low-latency streaming
CHUNK_SIZE = 64 * 1024

def parse_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    """
    Parses 'Range: bytes=start-end' header and validates offsets.
    Raises HTTPException 416 if requested range cannot be satisfied.
    """
    match = re.match(r"^bytes=(\d*)-(\d*)$", range_header.strip())
    if not match:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Invalid Range header format",
            headers={"Content-Range": f"bytes */{file_size}"}
        )

    start_str, end_str = match.groups()

    if start_str and end_str:
        start = int(start_str)
        end = int(end_str)
    elif start_str:
        start = int(start_str)
        end = file_size - 1
    elif end_str:
        # Suffix range
        suffix_length = int(end_str)
        start = max(0, file_size - suffix_length)
        end = file_size - 1
    else:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Empty Range specifications",
            headers={"Content-Range": f"bytes */{file_size}"}
        )

    if start > end or start >= file_size:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail="Requested range out of bounds",
            headers={"Content-Range": f"bytes */{file_size}"}
        )

    end = min(end, file_size - 1)
    return start, end

def chunk_generator(file_path: str, start: int, end: int, chunk_size: int = CHUNK_SIZE) -> Generator[bytes, None, None]:
    """Reads byte chunks from file starting at `start` offset up to `end` inclusive."""
    bytes_remaining = (end - start) + 1
    with open(file_path, "rb") as f:
        f.seek(start)
        while bytes_remaining > 0:
            read_size = min(chunk_size, bytes_remaining)
            data = f.read(read_size)
            if not data:
                break
            bytes_remaining -= len(data)
            yield data

def get_media_stream_response(file_path: str, mime_type: str, range_header: Optional[str] = None) -> StreamingResponse:
    """
    Produces an HTTP StreamingResponse.
    Returns HTTP 206 Partial Content when Range header is provided,
    or HTTP 200 OK for full content delivery.
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media file not found on host disk")

    file_size = os.path.getsize(file_path)

    if range_header:
        start, end = parse_range_header(range_header, file_size)
        content_length = (end - start) + 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": mime_type,
            "Cache-Control": "no-cache",
        }
        return StreamingResponse(
            chunk_generator(file_path, start, end),
            status_code=status.HTTP_206_PARTIAL_CONTENT,
            headers=headers
        )
    else:
        # Full content streaming
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Type": mime_type,
            "Cache-Control": "no-cache",
        }
        return StreamingResponse(
            chunk_generator(file_path, 0, file_size - 1),
            status_code=status.HTTP_200_OK,
            headers=headers
        )
