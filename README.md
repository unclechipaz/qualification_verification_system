# Midlands State University Qualification Verification System

An academic Django application for registering graduate records, looking up certificates, recording verification activity and demonstrating employer screening. It provides server-rendered web pages and a Django REST Framework API.

**Documentation baseline:** source commit `0faeb043c8c2c602008b1c7e1d45eb29efdcd098`, reviewed on 10 September 2026. This baseline contains the CI repairs in PR #4, the authentication fixes in PR #6 and the documentation-branch synchronisation in PR #7. It is a development baseline; these merges do not establish production readiness or confirm the state of the hosted application.

## Implemented capabilities

| Requirement | Current behaviour |
| --- | --- |
| Register qualifications and certifications | Administrator/registrar users can create student records. Qualification definitions and certificates are separate records managed through the API or suitably authorised Django administration accounts. Creating a student through the web form does not issue a certificate. |
| Search and retrieve records | Verification searches certificate number, verification code, student number, national ID and then a partial name. It returns the first matching certificate. Administrative student and certificate API lists support `?search=`. |
| Verify qualifications | The result follows the stored certificate status: `ACTIVE → VERIFIED`, `REVOKED → REVOKED`, and `SUSPENDED → PENDING`; an unmatched identifier produces `INVALID`. The application generates QR images and PDF verification reports. |
| Maintain verification history | `VerificationLog` stores searches, results and heuristic risk scores. Employers can view/export their own logged checks. `AuditLog` records selected HTTP write requests and response status codes. |

## Current limits

- The **QR Scanner** page starts a camera preview and accepts manual identifiers. Automatic QR decoding and image-upload scanning are not implemented.
- The field named `digital_signature_hash` stores a SHA-256 digest of selected certificate fields. There is no signing key or verification-time digest comparison. The generated PDF is not cryptographically signed or protected against editing.
- `AIFraudDetector` is a fixed-rule scoring component, not a trained machine-learning model. A score is an indicator for review, not proof of fraud or an enforcement mechanism.
- The web result template does not yet display `PENDING` separately, and certificate pages/PDF downloads have access-control limitations described in the manuals.
- Deployment settings, dependency support, persistent storage and remaining controls need further work. See [deployment limitations](docs/INSTALLATION_GUIDE.md#deployment-status-and-remaining-work).

## Technology

| Area | Repository configuration |
| --- | --- |
| Runtime | Python 3.13 in GitHub Actions and the Docker image |
| Framework | `Django>=5.0,<5.2`; other dependency ranges are in [requirements.txt](requirements.txt) |
| Web interface | Django templates, Bootstrap 5.3, JavaScript |
| Database | SQLite by default; PostgreSQL selected using `DB_ENGINE`. Compose uses PostgreSQL 16. |
| Outputs | ReportLab PDF reports, qrcode/Pillow QR images, CSV exports |
| Verification | pytest and pytest-django; Django checks and migration-drift checks |
| Packaging | Docker development configuration and a Vercel WSGI entry point |

The Actions workflow checks Django configuration, checks for missing migrations, runs pytest and builds a Docker image. It does not currently lint the source, publish that image, deploy the application, or run a security/coverage gate.

## Getting started

Use the [Installation Guide](docs/INSTALLATION_GUIDE.md) for Windows PowerShell and Linux/macOS commands, a separate local demonstration database and Docker instructions. Clone the `develop` branch to obtain the merged application fixes:

```bash
git clone --branch develop https://github.com/unclechipaz/qualification_verification_system.git
cd qualification_verification_system
```

Use synthetic data for demonstrations. The seed command creates known-password demo accounts and resets those passwords every time it runs; its account details and exact effects are documented in the installation guide.

## Team responsibilities

These assignments describe responsibilities, not verified contribution counts.

| Member | Role | Main responsibility |
| --- | --- | --- |
| Charlton | Project Manager and DevOps Lead | Architecture, Django setup, repository management, containers, CI and deployment |
| Simba | Database and Qualification Registry Lead | Requirement 1: student, qualification and certificate data; migrations and seeding |
| Mncedisi (Artwell) | Search and Retrieval Specialist | Requirement 2: search logic, APIs and query indexing |
| Doreen | Verification and Frontend UI Specialist | Requirement 3: verification pages, status presentation and scanner interface |
| Cleopatra | Audit Trail and QA/Documentation Lead | Requirement 4: activity history, tests, manuals and diagrams |

## Documentation

- [Architecture and implementation limits](docs/ARCHITECTURE.md)
- [API reference](docs/API_DOCUMENTATION.md)
- [Data model and UML diagrams](docs/UML_DIAGRAMS.md)
- [User Manual](docs/USER_MANUAL.md)
- [Administrator Manual](docs/ADMINISTRATOR_MANUAL.md)
- [Installation Guide](docs/INSTALLATION_GUIDE.md)
- [Contribution workflow](CONTRIBUTING.md)
- [Software requirements](REQUIREMENTS.md)
- [Database ERD and data dictionary](DATABASE_ERD.md)
- [Requirements traceability matrix](REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [Testing and verification plan](TESTING_AND_VERIFICATION.md)
- [Deployment and release guide](DEPLOYMENT_GUIDE.md)
- [Security and privacy policy](SECURITY.md)
The reviewed repository does not contain a licence file; no software licence is asserted here.
