"""
Utility script to generate sample audio and test files for immediate testing and demonstration.
"""

import os
import wave
import struct
import math

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_media")

def create_sample_wav(filename: str, duration_sec: int = 5, frequency: float = 440.0):
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    file_path = os.path.join(SAMPLE_DIR, filename)

    sample_rate = 44100
    num_samples = int(duration_sec * sample_rate)

    with wave.open(file_path, "w") as wav_file:
        # 1 channel (mono), 2 bytes (16 bit), sample_rate, num_samples, 'NONE', 'not compressed'
        wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))
        
        for i in range(num_samples):
            # Generate a pleasant fading sine tone
            t = float(i) / sample_rate
            value = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * t))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

    print(f"Created sample audio: {file_path} ({duration_sec}s, {os.path.getsize(file_path)} bytes)")
    return file_path

def create_sample_video_stub(filename: str, size_bytes: int = 1024 * 1024):
    """Creates a binary video file stub for range-streaming testing."""
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    file_path = os.path.join(SAMPLE_DIR, filename)
    with open(file_path, "wb") as f:
        # Write repeating binary patterns to simulate streamable payload
        pattern = b"MP4_STREAM_TEST_DATA_FRAME_SEA_WATERFALL_2026_" * 64
        written = 0
        while written < size_bytes:
            f.write(pattern)
            written += len(pattern)
    print(f"Created sample video test file: {file_path} ({os.path.getsize(file_path)} bytes)")
    return file_path

if __name__ == "__main__":
    create_sample_wav("sample_synth_melody.wav", duration_sec=6, frequency=440.0)
    create_sample_wav("sample_acoustic_chime.wav", duration_sec=4, frequency=587.33)
    create_sample_video_stub("sample_nature_clip.mp4", size_bytes=512 * 1024)
    create_sample_video_stub("sample_ocean_documentary.mkv", size_bytes=1024 * 1024)
    print("All sample media successfully generated in:", SAMPLE_DIR)
