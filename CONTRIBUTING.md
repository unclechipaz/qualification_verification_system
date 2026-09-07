# Midlands State University - Qualification Verification System
## Group Contributions & Team Role Assignments

This repository represents the collaborative Software Engineering Group Assignment for Midlands State University (MSU).

### Core System Requirements & Team Member Assignments

| Member Name | Assigned Role | Core Requirement & Modules Assigned |
| :--- | :--- | :--- |
| **Charlton** | **Project Manager & DevOps Lead** | Overall System Architecture, Django Core Configuration, Git Repository Management, Docker Containerization, CI/CD Pipeline (`.github/workflows/ci_cd.yml`), Vercel/Render Cloud Deployment. |
| **Simba** | **Database & Qualification Registry Lead** | **Requirement 1: Register Qualifications & Certifications**. Database Schema Design, Django ORM Models (`Student`, `Qualification`, `Certificate`), Database Migrations, and Automated Seeding Script (`seed_db.py`). |
| **Mncendisi** | **Search & Retrieval Specialist** | **Requirement 2: Search & Retrieve Qualification Records**. Multi-parameter Search Engine (`Certificate Number`, `Student Number`, `National ID`, `Name`), REST API Endpoints (`/api/students/`, `/api/qualifications/`), and Database Query Indexing. |
| **Doreen** | **Verification & Frontend UI Specialist** | **Requirement 3: Verify Authenticity of Qualifications**. Public & Employer Verification Web Portals, Bootstrap 5 MSU Theme Layout, WebCam QR Code Scanner UI, Verification Status Stamps (`VERIFIED`, `REVOKED`, `INVALID`). |
| **Cleopatra** | **Audit Trail & QA/Documentation Lead** | **Requirement 4: Maintain Auditable History of Verification Activities**. Audit Logging Middleware (`AuditLog`), Screening History Tracking, Pytest Automated Test Suite (`tests/`), System Manuals, and UML Diagrams. |

---

### Workflow Guidelines

1. **Branching Strategy**:
   - `main`: Production-ready, stable releases.
   - `develop`: Integration branch for active development.
   - `feature/*`: Specific feature branches assigned per member (e.g. `feature/registration`, `feature/search`, `feature/verification`, `feature/audit-logs`).

2. **Commit Standard**:
   - Use imperative mood: `Add Verification REST API endpoint`
   - Include component scope prefix: `[Students] Implement student registration serializer`

3. **Pull Requests & Code Reviews**:
   - All feature branches must be merged into `develop` via Pull Request before merging to `main`.
