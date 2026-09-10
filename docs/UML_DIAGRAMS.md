# MSU QVS: Data Model and System Diagrams

**Source baseline:** `0faeb043c8c2c602008b1c7e1d45eb29efdcd098`, reviewed on 10 September 2026.

These diagrams describe selected parts of the current implementation. They do not certify that all intended controls or deployment components are implemented.

## 1. Entity relationships

Fields below are selected model fields. Inherited Django authentication fields and some timestamps are omitted for readability.

```mermaid
erDiagram
    USER |o--o| STUDENT : "optional linked account"
    USER ||--o| EMPLOYER : "company profile"
    STUDENT ||--o| CERTIFICATE : "issued certificate"
    QUALIFICATION ||--o{ CERTIFICATE : "defines"
    CERTIFICATE |o--o{ VERIFICATION_LOG : "lookup target"
    USER |o--o{ VERIFICATION_LOG : "requesting account"
    USER |o--o{ AUDIT_LOG : "requesting account"

    USER {
        bigint id PK
        string username UK
        string role
        string national_id UK "nullable"
        boolean is_verified_employer
        boolean is_staff
    }
    STUDENT {
        bigint id PK
        bigint user_id FK,UK "nullable"
        string student_number UK
        string national_id UK
        string full_name
        string programme
        string qualification "text field"
        date graduation_date
        string status
    }
    EMPLOYER {
        bigint id PK
        bigint user_id FK,UK
        string company_name
        string contact_person
        string contact_email
        boolean is_verified_company
    }
    QUALIFICATION {
        bigint id PK
        string title
        string code UK
        string faculty
        string department
        int duration_years
    }
    CERTIFICATE {
        bigint id PK
        bigint student_id FK,UK
        bigint qualification_id FK
        string certificate_number UK
        string verification_code UK
        date issue_date
        string status
        string digital_signature_hash
        string qr_code_image
        string revocation_reason
    }
    VERIFICATION_LOG {
        bigint id PK
        bigint certificate_id FK "nullable"
        bigint verified_by_id FK "nullable"
        string search_query
        string search_type
        string result_status
        string ip_address
        boolean is_suspicious
        int anomaly_score
        string fraud_reason
        datetime timestamp
    }
    AUDIT_LOG {
        bigint id PK
        bigint user_id FK "nullable"
        string action
        string target
        string ip_address
        string details
        datetime timestamp
    }
```

A student may have no login account and no certificate. Each existing certificate requires one student and one qualification definition. `Student.qualification` is free text, so there is no direct student-to-qualification foreign key.

| Deleted object | Relationship behaviour |
| --- | --- |
| User | Linked student's user field and log user fields become null; an employer profile is deleted. |
| Student | Its certificate is deleted. |
| Certificate | Existing verification logs retain their other fields, with certificate set to null. |
| Qualification with certificates | Deletion is protected. |

These relationships are defined in the [student](../backend/students/models.py), [qualification/certificate](../backend/qualifications/models.py), [employer](../backend/employers/models.py), [verification-log](../backend/verification/models.py) and [audit-log](../backend/audit/models.py) models.

## 2. Principal user activities

This flowchart maps the main actors to supported tasks; it is a use-case overview, not a complete access-control model.

```mermaid
flowchart TD
    Public["Public verifier"]
    Employer["Employer"]
    Graduate["Graduate"]
    Staff["Administrator or registrar"]
    Verify["Submit verification"]
    History["View own screening history"]
    Profile["View linked graduate profile"]
    Registry["Manage registry through API or admin"]
    Analytics["Review reports and anomaly logs"]
    Public --> Verify
    Employer --> Verify
    Employer --> History
    Graduate --> Profile
    Staff --> Registry
    Staff --> Analytics
```

Django administration additionally requires staff/model permissions. The registry and certificate-detail web pages currently allow any logged-in account, and the PDF route has no authentication or ownership check. Those limits are documented in the [Administrator Manual](ADMINISTRATOR_MANUAL.md).

The scanner page offers camera preview and manual input; automated QR decoding is not represented as a completed use case.

## 3. Verification and PDF sequence

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant View as Django or DRF view
    participant Risk as Heuristic detector
    participant DB as Database
    participant PDF as ReportLab
    Client->>View: Submit identifier
    View->>DB: Look up first matching certificate
    DB-->>View: Certificate or no match
    View->>Risk: Evaluate identifier, status, IP and user agent
    Risk->>DB: Count recent logs for the IP
    DB-->>Risk: Earlier request count
    Risk-->>View: Score, flag and reasons
    View->>View: Map certificate status to result
    View->>DB: Create VerificationLog
    View-->>Client: HTML result or JSON response
    opt Download verification report
        Client->>View: Request PDF by log ID
        View->>DB: Read log and current certificate/student
        DB-->>View: Report data
        View->>PDF: Build verification report
        PDF-->>View: PDF bytes
        View-->>Client: PDF download
    end
```

Web verification can additionally generate a stored QR image if one is absent. There is no signature-check step, and PDF generation does not create an immutable historical snapshot.

## 4. Result decision

```mermaid
flowchart TD
    Query["Nonempty verification query"] --> Match{"Certificate found?"}
    Match -->|No| Invalid["INVALID"]
    Match -->|Yes| Status{"Certificate status"}
    Status -->|ACTIVE| Valid["VERIFIED"]
    Status -->|REVOKED| Revoked["REVOKED"]
    Status -->|SUSPENDED| Pending["PENDING"]
```

This describes service behaviour. The current web template lacks a separate `PENDING` panel and displays its generic invalid/not-found result instead.

## 5. Included Docker development topology

```mermaid
flowchart TD
    Browser["Browser on developer computer"]
    Source["Host source directory"]
    subgraph Compose["Docker Compose"]
        Web["Python 3.13 and Django runserver"]
        DB[("PostgreSQL 16")]
    end
    Volume[("postgres_data volume")]
    Browser -->|"HTTP on port 8000"| Web
    Source -->|"Bind mount at /app"| Web
    Web -->|"Database connection on port 5432"| DB
    DB --> Volume
```

The supplied Compose file also publishes the database port to the host. Its entrypoint runs migrations and demonstration seeding on startup. It does not include Gunicorn, a reverse proxy or TLS termination as running services.

The separate Vercel configuration exposes Django through `index.py`. Its temporary-file behaviour and remaining deployment work are described in the [Installation Guide](INSTALLATION_GUIDE.md#deployment-status-and-remaining-work).
