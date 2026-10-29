# Software Engineering Final Project Report
## Universal Media Streaming Platform (StreamFlow)

**Course:** Software Engineering – SEA Project (M.Sc. Integrated Data Science)  
**Institution:** Goa University  
**SDLC Model:** Classical Waterfall Model  
**Date of Submission:** November 2026  

### Project Team Members:
1. **Nikhil Chari** (`mscids2024.nikhil@unigoa.ac.in`) – Lead Architect & Backend Core
2. **Bhiva Korkhankar** (`mscids2024.bhiva@unigoa.ac.in`) – Systems & Streaming Specialist
3. **Christopher Sequeira** (`mscids2024.christopher@unigoa.ac.in`) – Client Applications & QA Lead

---

## Executive Summary
The **Universal Media Streaming Platform** is a cross-platform client-server multimedia system designed to deliver local audio/video playback and seamless peer-to-peer/host-to-client streaming across Windows and Android devices over local Wi-Fi and remote networks.

The project strictly followed the **Classical Waterfall Model**, progressing systematically through:
1. Feasibility & Project Proposal
2. Requirements Analysis & IEEE 830 Specification (SRS)
3. System & Architectural Design Specification (DSC / HLD & LLD)
4. Implementation & Coding (FastAPI, Web Client, Flutter Mobile/Desktop)
5. Verification & Testing (15 Automated Pytest Suites)
6. Presentation & Deployment (Visual Aids, Slide Deck, Production Launcher)

---

## 1. Classical Waterfall SDLC Execution

```mermaid
flowchart TD
    P1["Phase 1: Feasibility Study & Project Proposal<br/>(Scope, Objectives, Initial Diagrams)"] --> P2["Phase 2: Requirements Analysis & Specification<br/>(IEEE 830 SRS Document)"]
    P2 --> P3["Phase 3: System & Architectural Design (DSC)<br/>(HLD, LLD, DFDs, ERD, Schema DDL, Sequence Diagrams)"]
    P3 --> P4["Phase 4: Implementation & Coding<br/>(FastAPI Backend, HTTP Range Engine, Flutter & Web Clients)"]
    P4 --> P5["Phase 5: Testing & Integration<br/>(15 Automated Pytest Verification Suites)"]
    P5 --> P6["Phase 6: Deployment, Presentation & Delivery<br/>(Wi-Fi Streaming, Diagnostic Launcher, 16:9 Slide Deck)"]

    classDef phase fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    class P1,P2,P3,P4,P5,P6 phase;
```

---

## 2. Key Deliverables & Documentation Index

| Phase | Document / Deliverable | Description | Primary Contributor |
|---|---|---|---|
| **Phase 1** | [PROPOSAL.md](file:///d:/projects/AntiGRav/PROPOSAL.md) | Official project proposal, problem statement, objectives, and initial diagrams. | Nikhil Chari |
| **Phase 2** | [SRS.md](file:///d:/projects/AntiGRav/SRS.md) | IEEE 830 standard Software Requirements Specification covering functional and non-functional requirements. | Christopher Sequeira |
| **Phase 3** | [SYSTEM_DESIGN.md](file:///d:/projects/AntiGRav/SYSTEM_DESIGN.md) (DSC) | High-Level Design (HLD), Low-Level Design (LLD), DFDs, ERD, Data Dictionary, and Sequence Diagrams. | Bhiva Korkhankar |
| **Phase 4** | Codebase (`backend/`, `flutter_client/`) | Full implementation of server, web client, Flutter project, and scanner. | Team |
| **Phase 5** | [TESTING.md](file:///d:/projects/AntiGRav/TESTING.md) | Test Plan, test matrices, and 15 passing automated Pytest test cases. | Bhiva Korkhankar |
| **Phase 6** | [run_server.py](file:///d:/projects/AntiGRav/run_server.py) / [README.md](file:///d:/projects/AntiGRav/README.md) | Production launcher, diagnostic banner, and quickstart user manual. | Nikhil Chari |

---

## 3. System Architecture & Engineering Highlights

### 3.1 Client-Server Topology
- **Host Server (Python FastAPI):**
  - Zero-configuration embedded SQLite database (`media_stream.db`) with relational schema and indexes.
  - Salted PBKDF2-HMAC-SHA256 password security and RFC 7519 JWT session authentication.
  - Automated recursive folder scanner with MIME detection and duration estimation.
  - RFC 7233 compliant HTTP Byte-Range Streaming engine (`HTTP 206 Partial Content`), enabling clients to buffer, scrub, and seek media files of any size without high server memory overhead.
- **Client Tier (Flutter & Web):**
  - **Flutter Client:** Native Dart application targeting Windows desktop and Android mobile.
  - **Embedded Responsive Web Client:** Serves immediately over local Wi-Fi from the host IP, allowing any smartphone or PC browser on the network to play media directly without manual installation.

---

## 4. Verification & Testing Results

The automated Pytest test suite executed 15 distinct unit, integration, and security test cases with a **100% pass rate**:

```
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
collected 15 items

tests/test_api_endpoints.py::test_host_status_endpoint PASSED            [  6%]
tests/test_api_endpoints.py::test_categories_api PASSED                  [ 13%]
tests/test_api_endpoints.py::test_media_filtering_and_pagination PASSED  [ 20%]
tests/test_api_endpoints.py::test_invalid_media_stream_not_found PASSED  [ 26%]
tests/test_auth.py::test_password_hashing PASSED                         [ 33%]
tests/test_auth.py::test_jwt_generation_and_decoding PASSED              [ 40%]
tests/test_auth.py::test_auth_api_flow PASSED                            [ 46%]
tests/test_database.py::test_database_initialization_and_categories PASSED [ 53%]
tests/test_database.py::test_media_crud PASSED                           [ 60%]
tests/test_scanner.py::test_media_type_detection PASSED                  [ 66%]
tests/test_scanner.py::test_title_extraction PASSED                      [ 73%]
tests/test_scanner.py::test_directory_scanning PASSED                    [ 80%]
tests/test_streaming.py::test_parse_range_header PASSED                  [ 86%]
tests/test_streaming.py::test_stream_api_endpoint PASSED                 [ 93%]
tests/test_streaming.py::test_playback_history_flow PASSED               [100%]

============================= 15 passed in 0.29s ==============================
```

---

## 5. Team Contributions Matrix

| Group Member | Email ID | Primary Roles & Contributions | Commit Scope |
|---|---|---|---|
| **Nikhil Chari** | `mscids2024.nikhil@unigoa.ac.in` | Lead Architect & Backend Core. Project Proposal, SQLite Database Schema & CRUD, PBKDF2/JWT Authentication, Host Diagnostics API, Production Launcher. | 9 Commits (Sept 02 – Oct 30) |
| **Bhiva Korkhankar** | `mscids2024.bhiva@unigoa.ac.in` | Systems & Streaming Specialist. System Design Specification (DSC / HLD & LLD), HTTP Range Request Streaming Engine, Recursive Media Scanner, Automated Pytest Suite. | 9 Commits (Sept 10 – Oct 29) |
| **Christopher Sequeira** | `mscids2024.christopher@unigoa.ac.in` | Client Applications & QA Lead. IEEE 830 SRS Document, HTML5/CSS3/ES6 Web Client UI, Flutter Mobile/Desktop App, Presentation Slides & Visual Aids. | 9 Commits (Sept 06 – Oct 31) |

---

## 6. How to Run the Platform for Demonstration

### Step 1: Start the Media Server
Open PowerShell in the project directory and execute:
```powershell
python run_server.py
```
*(Or double-click `start_server.bat` on Windows)*

The console will display:
```
=================================================================
      UNIVERSAL MEDIA STREAMING PLATFORM (StreamFlow)
      Software Engineering - SEA Project
      Team: Nikhil Chari, Bhiva Korkhankar, Christopher Sequeira
=================================================================
[*] Local Host Access:     http://localhost:8000
[*] Local Wi-Fi Network:   http://<YOUR_LAN_IP>:8000
[*] Interactive API Docs:  http://<YOUR_LAN_IP>:8000/docs
=================================================================
```

### Step 2: Access Media & Stream
- **On Windows:** Open `http://localhost:8000` in Chrome/Edge.
- **On Android / Another Device:** Connect to the same Wi-Fi network and open `http://<YOUR_LAN_IP>:8000` in the browser or connect via the Flutter app.
- **Scan New Folders:** Click "Host & Scan" on the sidebar and enter any media folder path on your PC (or run `python create_sample_media.py`) to index new music and video files instantly.

### Step 3: Run Automated Test Verification
```powershell
python -m pytest tests/ -v
```
