# Universal Media Streaming Platform (StreamFlow)

**Software Engineering – SEA Project (M.Sc. Integrated Data Science)**  
**Institution:** Goa University  
**SDLC Model:** Classical Waterfall Model  
**Team Members & Roles:**
- **Nikhil Chari** (`mscids2024.nikhil@unigoa.ac.in`) – Lead Architect & Backend Core
- **Bhiva Korkhankar** (`mscids2024.bhiva@unigoa.ac.in`) – Systems & Streaming Specialist
- **Christopher Sequeira** (`mscids2024.christopher@unigoa.ac.in`) – Client Applications & QA Lead  

A cross-platform multimedia solution enabling local media playback and HTTP byte-range audio/video streaming across Windows and Android devices over Wi-Fi and remote networks.

---

## 📚 Complete Waterfall Documentation Suite

1. **Phase 1: Project Proposal & Feasibility** ➔ [PROPOSAL.md](PROPOSAL.md)
   - Problem Statement, Objectives, Tech Stack, Use Case Diagram, DFD L0, DFD L1, and ERD.
2. **Phase 2: Requirements Analysis & Specification** ➔ [SRS.md](SRS.md)
   - IEEE 830 compliant Software Requirements Specification with functional & non-functional requirements.
3. **Phase 3: System & Architectural Design** ➔ [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md)
   - High-Level Architecture, Low-Level Design, Relational SQLite Schema DDL, REST API endpoints, and Sequence Diagrams.
4. **Phase 5: Software Test Plan & Verification** ➔ [TESTING.md](TESTING.md)
   - Test Plan Matrix and 15 passing automated Pytest test cases.
5. **Phase 6: Final Academic Report** ➔ [PROJECT_REPORT.md](PROJECT_REPORT.md)
   - Comprehensive Software Engineering submission report synthesized from Proposal, SRS, DSC, and Test matrices.

---

## 🚀 Quick Start Guide

### 1. Launch the Media Server
Run the launcher script:
```powershell
python run_server.py
```
*(Or double-click `start_server.bat`)*

### 2. Stream Media
- Open `http://localhost:8000` on Windows.
- Open `http://<YOUR_LAN_IP>:8000` on your Android phone or any device on the same Wi-Fi network.
- Interactive Swagger API Documentation is available at `http://localhost:8000/docs`.

### 3. Run Automated Tests
```powershell
python -m pytest tests/ -v
```

---

## 🏗️ Technology Stack
- **Backend:** Python FastAPI, Uvicorn, SQLite 3, PBKDF2-HMAC-SHA256, RFC 7519 JWT, RFC 7233 HTTP Byte-Range Streaming
- **Frontend:** Flutter (Windows / Android) & Embedded Responsive HTML5/ES6 Web Client
- **Testing:** Pytest, HTTPX TestClient
