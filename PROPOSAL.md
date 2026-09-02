# Project Proposal: Universal Media Streaming Platform

**Course:** Software Engineering – SEA Project (M.Sc. Integrated Data Science)  
**Institution:** Goa University  
**SDLC Model:** Classical Waterfall Model  
**Date:** September 2026  
**Group Members:**
1. **Nikhil Chari** (`mscids2024.nikhil@unigoa.ac.in`)
2. **Bhiva Korkhankar** (`mscids2024.bhiva@unigoa.ac.in`)
3. **Christopher Sequeira** (`mscids2024.christopher@unigoa.ac.in`)

---

## 1. Introduction
The **Universal Media Streaming Platform** is a cross-platform media solution designed to allow users to play local audio and video files and stream media seamlessly between devices. The system supports Windows and Android platforms, enabling media sharing over local Wi-Fi networks as well as remote internet connections.

---

## 2. Problem Statement
Users frequently depend on multiple disparate applications to play and transfer media across different devices. Transferring high-definition media files over physical storage or cloud drives is often slow, cumbersome, and impractical. This project addresses these pain points by offering a unified client-server platform where users can instantly browse, access, and stream shared media files across devices without manual transfers.

---

## 3. Objectives
- **Cross-Platform Playback:** Develop a responsive media player for Windows and Android using Flutter.
- **Local Playback:** Support offline playback for audio and video formats.
- **Media Hosting & Sharing:** Enable any host device (e.g., Windows PC) to serve media across the network.
- **Network Streaming:** Provide smooth HTTP range-based streaming over local Wi-Fi and remote connections.
- **Secure Access Control:** Implement user authentication and session management.
- **Intuitive UI:** Offer an accessible, clean, and user-friendly interface.

---

## 4. Proposed System Architecture
The platform is built on a **Client-Server Architecture**:
- **Frontend (Flutter):** Provides the cross-platform UI on Windows and Android for media discovery, playback controls, host connections, and history tracking.
- **Backend (Python FastAPI):** Serves RESTful APIs, handles user authentication, exposes HTTP byte-range streaming endpoints, and scans local file directories.
- **Database (SQLite):** Lightweight, serverless relational database managing user accounts, media metadata, categories, and playback history.

```mermaid
graph LR
    subgraph Client["Client Tier (Flutter)"]
        UI["Flutter UI (Windows / Android)"]
        Player["ExoPlayer / VideoPlayer Controller"]
    end

    subgraph Server["Server Tier (Python FastAPI)"]
        API["FastAPI REST Endpoints"]
        Auth["Auth & JWT Service"]
        StreamEngine["HTTP Byte-Range Streaming Engine"]
    end

    subgraph DataStore["Data & Media Storage"]
        DB[(SQLite Database)]
        FileSystem[("Local Storage / Media Folders")]
    end

    UI -->|HTTP Requests / Auth| API
    Player -->|HTTP Audio/Video Stream| StreamEngine
    API --> Auth
    API --> DB
    StreamEngine --> FileSystem
```

---

## 5. Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Frontend** | Flutter (Dart) | Single codebase for Windows and Android with native performance |
| **Backend** | Python FastAPI | Asynchronous high-performance framework, native support for byte-range streaming |
| **Database** | SQLite (with SQLAlchemy) | Embedded, zero-configuration relational database ideal for local media servers |
| **Streaming Protocol** | HTTP Range Requests (RFC 7233) | Enables seeking, scrubbing, and lightweight streaming over standard HTTP |
| **Testing** | Pytest & Flutter Test | Automated backend unit/integration testing and client widget testing |
| **Version Control** | Git & GitHub | Collaborative version control and milestone tracking |

---

## 6. SDLC Model: Classical Waterfall Model

The project strictly follows the **Classical Waterfall Model** with sequential phases:

```mermaid
flowchart TD
    A["1. Requirements Analysis & Specification"] --> B["2. System & Architectural Design"]
    B --> C["3. Implementation & Unit Testing"]
    C --> D["4. Integration & System Testing"]
    D --> E["5. Deployment & User Acceptance"]
    E --> F["6. Maintenance & Documentation"]
```

---

## 7. System Diagrams

### 7.1 Diagram 1 – UML Use Case Diagram

```mermaid
flowchart LR
    User(["👤 User"]):::actor
    Host(["👤 Media Host"]):::actor

    subgraph Platform ["Universal Media Streaming Platform Boundary"]
        UC1(["Browse Media"])
        UC2(["Play Audio / Video"])
        UC3(["Control Playback"])
        UC4(["Connect to Server"])
        UC5(["Stream Media"])
        UC6(["Start Media Server"])
        UC7(["Manage Shared Media"])
        UC8(["Authenticate User"])
    end

    User --> UC8
    User --> UC4
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC5

    Host --> UC8
    Host --> UC6
    Host --> UC7
    Host --> UC5

    classDef actor fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b;
```

#### Actor & Use Case Specifications

| Actor | Responsibilities |
|---|---|
| **User** | Connects to active media server, browses catalog, controls audio/video playback, and views playback history. |
| **Media Host** | Starts the media server daemon, specifies directories to share, manages access permissions, and streams media. |

---

### 7.2 Diagram 2 – Data Flow Diagram (DFD) Level 0 (Context Diagram)

```mermaid
flowchart LR
    User["👤 User / Client"]
    Host["💻 Windows Media Host"]
    System(("0.0<br/>Universal Media<br/>Streaming Platform"))

    User -->|Credentials & Connection Requests| System
    User -->|Media Selection & Playback Commands| System
    System -->|Auth Token & Media Catalog| User
    System -->|HTTP Audio/Video Stream| User

    Host -->|Shared Directory Paths & Files| System
    Host -->|Media Metadata & Server Config| System
    System -->|Media Access Logs & Stream Status| Host
```

---

### 7.3 Diagram 3 – Data Flow Diagram (DFD) Level 1 (Internal Processes)

```mermaid
flowchart TD
    User["👤 User / Client"]
    Host["💻 Windows Media Host"]

    P1(("1.0<br/>User Authentication"))
    P2(("2.0<br/>Browse Media"))
    P3(("3.0<br/>Request Media"))
    P4(("4.0<br/>Stream Media"))
    P5(("5.0<br/>Playback Control"))

    D1[("D1: User Database")]
    D2[("D2: Media Metadata Database")]
    D3[("D3: Local Media Files")]

    %% Process 1.0
    User -->|Login Credentials| P1
    P1 <-->|Verify / Store User Records| D1
    P1 -->|Auth Token / Status| User

    %% Process 2.0
    User -->|Browse Request / Category Filter| P2
    P2 <-->|Fetch Metadata / Categories| D2
    P2 -->|Media Catalog List| User

    %% Process 3.0
    User -->|Select Media Item| P3
    P3 <-->|Lookup File Path & Details| D2
    P3 -->|Stream Session Setup| P4

    %% Process 4.0
    Host -->|Register Media Directories| D2
    Host -->|Provide Media Files| D3
    D3 -->|Raw Byte Stream| P4
    P4 -->|HTTP Byte-Range Audio/Video Stream| User

    %% Process 5.0
    User -->|Play, Pause, Seek, Volume| P5
    P5 -->|Update Last Position & History| D1
```

---

### 7.4 Diagram 4 – Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o{ PLAYBACK_HISTORY : "has"
    MEDIA ||--o{ PLAYBACK_HISTORY : "appears_in"
    MEDIA_CATEGORY ||--o{ MEDIA : "contains"

    USER {
        int user_id PK "Auto Increment"
        string username "Unique"
        string password_hash "Hashed password"
        string email "Unique"
        datetime created_at "Timestamp"
    }

    MEDIA_CATEGORY {
        int category_id PK "Auto Increment"
        string category_name "e.g. Movies, Music, Podcasts"
        string description "Optional description"
    }

    MEDIA {
        int media_id PK "Auto Increment"
        string title "Media title"
        string file_path "Absolute path on host"
        string media_type "audio or video"
        int duration "Duration in seconds"
        int file_size "File size in bytes"
        int category_id FK "References MEDIA_CATEGORY"
        datetime added_at "Timestamp"
    }

    PLAYBACK_HISTORY {
        int history_id PK "Auto Increment"
        int user_id FK "References USER"
        int media_id FK "References MEDIA"
        datetime played_at "Last accessed timestamp"
        int last_position "Last played position in seconds"
        boolean completed "Playback completion flag"
    }
```

---

## 8. Expected Outcome & Deliverables
1. **FastAPI Media Server:** Fully functional server providing REST endpoints for auth, metadata indexing, and HTTP range streaming.
2. **Flutter Media Player App:** Native Windows desktop and Android mobile app with responsive UI, playback controls, seek bar, and server discovery.
3. **Database Layer:** SQLite database preconfigured with schema migrations, relational constraints, and seed data.
4. **Waterfall Documentation Suite:** Complete SRS document, System Architecture Document, Test Plan with Pytest test cases, and final project report.
