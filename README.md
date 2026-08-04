# Midlands State University (MSU) Qualification Verification System

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django 5.0](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD Pipeline](https://github.com/midlands-state-university/qualification-verification-system/actions/workflows/ci_cd.yml/badge.svg)](.github/workflows/ci_cd.yml)

A secure, production-ready Qualification Verification System developed for Midlands State University (MSU). The web application enables employers, universities, government institutions, and graduates to instantly verify academic credentials, detect fraud, inspect cryptographic digital hashes, and download official PDF verification statements.

---

## 🎓 Key Features

1. **Multi-Role Authentication & Access Control (RBAC)**:
   - Administrator, Registrar, Graduate, Employer, and Public Verifier roles.
2. **Student & Credential Management**:
   - Register graduates with Student Number, National ID, Full Name, Programme, Faculty, Degree Classification, and Graduation Date.
3. **Cryptographic Certificate Engine**:
   - Automatic generation of unique Certificate Numbers (`MSU-2024-BSC-CS-0001`), Verification Codes, SHA-256 integrity hashes, and QR codes.
4. **Multi-Parameter Verification**:
   - Verify credentials via Certificate Number, Student ID, Verification Code, National ID, Name, or Live Camera QR Code Scanner.
5. **AI Fraud Detection Engine**:
   - Automated anomaly detection identifying burst IP rate scanning, search attempts on revoked credentials, and suspect client signatures.
6. **Dynamic PDF Generation**:
   - Official printable PDF Verification Reports and Degree Certificates generated via ReportLab.
7. **DevOps & Cloud Ready**:
   - `Dockerfile`, `docker-compose.yml` (PostgreSQL + Django), GitHub Actions CI/CD pipeline (`.github/workflows/ci_cd.yml`), and pre-seeded database.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Django 5.x, Django REST Framework (DRF)
- **Frontend**: HTML5, Bootstrap 5.3, JavaScript (HTML5 WebCam QR Scanner)
- **Database**: PostgreSQL 16 (SQLite3 fallback)
- **Document Processing**: ReportLab (PDF), Pillow, qrcode
- **Testing**: Pytest, Django Test Framework
- **DevOps**: Docker, Docker Compose, GitHub Actions CI/CD

---

## 👥 Group Contributions & Roles

| Member Name | Role | Core Responsibility |
| :--- | :--- | :--- |
| **Charlton** | Project Manager & DevOps Lead | Backend Core Architecture, Docker, CI/CD, Git Workflow |
| **Collen Simba** | Database Architect & Models | Schema Design, ORM Models, Database Seeding |
| **Doreen** | Frontend & UI/UX Specialist | Bootstrap 5 Design, Templates, QR Scanner UI |
| **Artwell** | QA & Documentation Lead | Automated Pytest Suite, UML Diagrams, User/Admin Manuals |
| **Anesu** | API & Integration Developer | DRF REST APIs, AI Fraud Engine, ReportLab PDF Generator |

---

## 🚀 Quick Execution Guide

```bash
# Clone the repository
git clone https://github.com/midlands-state-university/qualification-verification-system.git
cd qualification_verification_system

# Install dependencies
pip install -r requirements.txt

# Migrate and Seed Database
python backend/manage.py migrate
python backend/manage.py seed_db

# Run Development Server
python backend/manage.py runserver 0.0.0.0:8000
```
Open `http://localhost:8000/` in your browser.

---

## 🔐 Default Demo Accounts

| Role | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin` | `AdminPass123!` |
| **Registrar** | `registrar` | `RegistrarPass123!` |
| **Employer** | `employer1` | `EmployerPass123!` |
| **Graduate** | `graduate1` | `GraduatePass123!` |

---

## 📖 Documentation Index

- [System Architecture](docs/ARCHITECTURE.md)
- [REST API Documentation](docs/API_DOCUMENTATION.md)
- [Database ER Diagram](docs/DATABASE_ERD.md)
- [System UML Diagrams](docs/UML_DIAGRAMS.md)
- [User Manual](docs/USER_MANUAL.md)
- [Administrator Manual](docs/ADMINISTRATOR_MANUAL.md)
- [Installation & Cloud Deployment Guide](docs/INSTALLATION_GUIDE.md)
- [Group Contributions Guide](CONTRIBUTING.md)
