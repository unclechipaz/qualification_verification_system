# Midlands State University - Qualification Verification System
## Group Contributions & Development Guidelines

This repository represents the collaborative Software Engineering Group Assignment for Midlands State University (MSU).

### Team Member Roles & Responsibilities

| Member Name | Primary Role | Assigned Modules & Tasks |
| :--- | :--- | :--- |
| **unclechipaz** | **Project Manager & DevOps Lead** | Project Architecture, Django Core setup, DevOps, Docker & Docker Compose, GitHub Actions CI/CD pipeline, Git workflow management. |
| **Collen Simba** | **Database Architect & Data Engineer** | Entity-Relationship (ER) Modeling, PostgreSQL schema design, Django ORM Models (Users, Students, Qualifications, Certificates, Logs), Seed database scripts. |
| **Doreen** | **Frontend Engineer & UI/UX Designer** | Bootstrap 5 UI design, Responsive HTML templates, Glassmorphism & MSU Theme styling, Interactive QR Scanner UI, Frontend Client Validation. |
| **Artwell** | **QA & Documentation Engineer** | Unit Testing, Integration Testing, API Endpoint Testing, System Documentation, User & Admin Manuals, UML Diagrams (Sequence, Class, Activity, Use Case, Deployment). |
| **Anesu** | **API Developer & Integration Specialist** | Django REST Framework (DRF) APIs, Verification Engine logic, AI Fraud Detection module, ReportLab PDF report generation, Deployment readiness. |

---

### Workflow Guidelines

1. **Branching Strategy**:
   - `main`: Production-ready, stable releases.
   - `develop`: Integration branch for active development.
   - `feature/*`: Specific feature branches (e.g. `feature/login`, `feature/verification`, `feature/api`).

2. **Commit Standard**:
   - Use imperative mood: `Add Verification REST API endpoint`
   - Include component scope prefix where appropriate: `[Students] Implement student registration serializer`

3. **Pull Requests & Code Reviews**:
   - All feature branches must be merged into `develop` via Pull Request.
   - GitHub Actions CI/CD must pass all automated tests (`pytest`) before merge approval.
