# Software Test Plan & Verification Matrix (TESTING.md)
## Universal Media Streaming Platform

**Course:** Software Engineering – SEA Project  
**SDLC Model:** Classical Waterfall Model  
**Phase:** Phase 5 – Testing & Verification  
**Testing Framework:** Pytest  
**Authors:** Nikhil Chari, Chrishtopher Sequeira, Bhiva Korkhankar

---

## 1. Test Objectives & Strategy
The testing phase verifies that the Universal Media Streaming Platform satisfies all functional and non-functional requirements specified in [SRS.md](file:///d:/projects/AntiGRav/SRS.md). Testing follows a multi-level strategy:
- **Unit Testing:** Validates cryptographic hashing, JWT encoding/decoding, SQLite CRUD operations, and byte-range math.
- **Integration Testing:** Tests interaction between the API routes, SQLite database, and local file storage.
- **Streaming & Protocol Verification:** Simulates HTTP Range requests (`Range: bytes=start-end`) to verify that the server returns HTTP `206 Partial Content`, `Content-Range`, and binary chunks accurately.

---

## 2. Test Environment
- **OS:** Windows 10/11
- **Python Version:** 3.10+
- **Testing Engine:** Pytest 9.x / HTTPX TestClient (Asynchronous HTTP testing)
- **Database:** Isolated SQLite in-memory or temporary test database (`test_media_stream.db`)

---

## 3. Test Cases Matrix

| Test Case ID | Test Category | Target Component | Description / Input | Expected Result | Status |
|---|---|---|---|---|---|
| **TC-AUTH-01** | Unit | Auth Service | Register a new user with valid details | User record created, hashed password stored, 201 Created | ✅ PASSED |
| **TC-AUTH-02** | Unit | Auth Service | Register duplicate username or email | Rejection with HTTP 400 Bad Request | ✅ PASSED |
| **TC-AUTH-03** | Unit | Auth Service | Login with correct username & password | HTTP 200 with valid JWT bearer token returned | ✅ PASSED |
| **TC-AUTH-04** | Unit | Auth Service | Login with incorrect password | HTTP 401 Unauthorized returned | ✅ PASSED |
| **TC-AUTH-05** | Security | Auth Service | Access protected endpoint without token | HTTP 401 Unauthorized returned | ✅ PASSED |
| **TC-SCAN-01** | Integration | Scanner | Scan directory containing `.mp4` and `.mp3` files | Media files detected with correct MIME and duration | ✅ PASSED |
| **TC-SCAN-02** | Integration | Scanner | Scan empty or non-existent folder | Graceful handling with 0 files added, no crash | ✅ PASSED |
| **TC-STREAM-01** | Protocol | Stream Dispatcher | Full file stream request (no Range header) | HTTP 200 OK with full file stream | ✅ PASSED |
| **TC-STREAM-02** | Protocol | Stream Dispatcher | Range request with `Range: bytes=0-499` | HTTP 206 Partial Content, exact 500 bytes delivered | ✅ PASSED |
| **TC-STREAM-03** | Protocol | Stream Dispatcher | Range request with seek offset `Range: bytes=1000-` | HTTP 206, starts at byte 1000 to EOF, Content-Range set | ✅ PASSED |
| **TC-STREAM-04** | Security | Stream Dispatcher | Request non-existent or invalid media ID | HTTP 404 Not Found returned | ✅ PASSED |
| **TC-HIST-01** | Functional | History Service | Update playback progress for a user | Record inserted/updated in `playback_history` | ✅ PASSED |
| **TC-HIST-02** | Functional | History Service | Fetch playback history for user | Returns list of played items with timestamps and positions | ✅ PASSED |
| **TC-HOST-01** | System | Host Diagnostics | Query `/api/host/status` | Returns system hostname, local IP, active port, status OK | ✅ PASSED |

---

## 4. Test Execution Summary

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

## 4. Execution Command
To execute the automated test suite:
```powershell
python -m pytest tests/ -v
```
