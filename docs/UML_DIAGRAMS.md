# Midlands State University QVS - System UML Diagrams

This document contains full Mermaid diagrams for all system models, software architecture, activity flows, and deployment topologies.

---

## 1. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o| STUDENT : "has profile"
    USER ||--o| EMPLOYER : "owns profile"
    USER ||--o{ VERIFICATION_LOG : "performs"
    STUDENT ||--o| CERTIFICATE : "owns"
    QUALIFICATION ||--o{ CERTIFICATE : "defines"
    CERTIFICATE ||--o{ VERIFICATION_LOG : "targeted in"
    USER ||--o{ AUDIT_LOG : "triggers"

    USER {
        int id PK
        string username
        string email
        string role
        string national_id
        boolean is_verified_employer
    }

    STUDENT {
        int id PK
        string student_number UK
        string national_id UK
        string full_name
        string programme
        string faculty
        date graduation_date
        string degree_classification
        string status
    }

    QUALIFICATION {
        int id PK
        string title
        string code UK
        string faculty
        int duration_years
    }

    CERTIFICATE {
        int id PK
        string certificate_number UK
        string verification_code UK
        date issue_date
        string status
        string digital_signature_hash
    }

    VERIFICATION_LOG {
        int id PK
        string search_query
        string search_type
        string result_status
        string ip_address
        boolean is_suspicious
        int anomaly_score
        datetime timestamp
    }
```

---

## 2. Use Case Diagram

```mermaid
graph TD
    PublicVerifier["Public Verifier"]
    Employer["Employer"]
    Graduate["Graduate"]
    Registrar["Registrar"]
    Admin["Administrator"]

    subgraph "MSU Qualification Verification System"
        UC1("Verify Certificate (Cert #, Student ID, QR Code)")
        UC2("Scan Certificate QR Code")
        UC3("Download PDF Verification Statement")
        UC4("Screen Candidates & View Verification History")
        UC5("Export Screening CSV Report")
        UC6("View Personal Digital Certificate")
        UC7("Register Graduate Student Record")
        UC8("Issue Digital Certificate & QR Code")
        UC9("Revoke / Suspend Certificate")
        UC10("Inspect AI Fraud Analytics")
        UC11("Manage System Users & Audit Logs")
    end

    PublicVerifier --> UC1
    PublicVerifier --> UC2
    PublicVerifier --> UC3

    Employer --> UC1
    Employer --> UC3
    Employer --> UC4
    Employer --> UC5

    Graduate --> UC6

    Registrar --> UC7
    Registrar --> UC8
    Registrar --> UC9
    Registrar --> UC10

    Admin --> UC7
    Admin --> UC9
    Admin --> UC10
    Admin --> UC11
```

---

## 3. Sequence Diagram (Verification Request & AI Threat Check)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Employer / Verifier
    participant Web as Django Web Server
    participant Detector as AI Fraud Detector
    participant DB as PostgreSQL Database
    participant PDF as ReportLab PDF Engine

    Client->>Web: Submit Verification Query (e.g. MSU-2024-BSC-CS-0001)
    Web->>DB: Query Certificate by Cert#, Student ID, or Code
    DB-->>Web: Return Certificate & Graduate Record
    Web->>Detector: Evaluate Query, IP, User Agent, & Status
    Detector-->>Web: Return (is_suspicious=False, score=0, reason="Normal")
    Web->>DB: Save VerificationLog Record
    Web-->>Client: Render Verification Result Page with Status Stamp
    Client->>Web: Request Download PDF Verification Report
    Web->>PDF: Generate Verification Report PDF Buffer
    PDF-->>Web: Return PDF Stream
    Web-->>Client: Download PDF File (MSU_Verification_Report_12.pdf)
```

---

## 4. Deployment Diagram

```mermaid
graph TB
    subgraph "Client Tier"
        Browser["Web Browser (Desktop / Mobile)"]
    end

    subgraph "Cloud / On-Premise Host (Docker Network)"
        Proxy["Nginx / Reverse Proxy (SSL/TLS HTTPS)"]
        
        subgraph "Application Container"
            Gunicorn["Gunicorn WSGI Application Server"]
            DjangoApp["Django 5.x Backend (MSU QVS Core)"]
        end
        
        subgraph "Database Container"
            Postgres["PostgreSQL 16 Relational DB"]
        end
    end

    Browser -->|HTTPS :443| Proxy
    Proxy -->|HTTP :8000| Gunicorn
    Gunicorn --> DjangoApp
    DjangoApp -->|TCP :5432| Postgres
```
