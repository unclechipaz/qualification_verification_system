# Midlands State University (MSU) Qualification Verification System

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Django 5.0](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD Pipeline](https://github.com/unclechipaz/qualification_verification_system/actions/workflows/ci_cd.yml/badge.svg)](.github/workflows/ci_cd.yml)

A secure, production-ready Qualification Verification System developed for Midlands State University (MSU). The web application enables employers, universities, government institutions, and graduates to instantly verify academic credentials, detect fraud, inspect cryptographic digital hashes, and download official PDF verification statements.

---

## 🎓 Core System Objectives & Features

1. **Register Qualifications or Certifications**:
   - Register graduates with Student Number, National ID, Full Name, Programme, Faculty, Degree Classification, and Graduation Date.
   - Automatic generation of unique Certificate Numbers (`MSU-2024-BSC-CS-0001`), Verification Codes, SHA-256 integrity hashes, and Base64 QR codes.
2. **Search and Retrieve Qualification Records**:
   - Multi-parameter search matching queries against Certificate Number, Student Number, Verification Code, National ID, or Full Name.
3. **Verify Authenticity of Qualifications**:
   - Live WebCam QR Code Scanner and instant verification portal returning statuses (`VERIFIED`, `REVOKED`, `INVALID`, `PENDING`).
   - AI Fraud Detection Engine computing an anomaly risk score (0–100) to detect suspicious scanning bursts or revoked credential checks.
4. **Maintain Auditable History of Verification Activities**:
   - Comprehensive `AuditLog` middleware tracking user actions, IP addresses, search queries, and timestamps.
   - Downloadable PDF Verification Statements and Employer Screening History CSV exports.

---

## 👥 Group Contributions & Roles (5 Team Members)

| Member Name | Role | Core Responsibility |
| :--- | :--- | :--- |
| **Charlton** | Project Manager & DevOps Lead | Architecture, Django Setup, Docker, CI/CD, Vercel Cloud Deployment |
| **Simba** | Database & Qualification Registry Lead | Requirement 1: Register Qualifications & Certifications, Database Schema, ORM Models, Seeding Script |
| **Mncendisi** | Search & Retrieval Specialist | Requirement 2: Search & Retrieve Qualification Records, Multi-parameter Search Logic, DRF APIs |
| **Doreen** | Verification & Frontend UI Specialist | Requirement 3: Verify Authenticity of Qualifications, Bootstrap 5 UI, WebCam QR Scanner |
| **Cleopatra** | Audit Trail & QA/Documentation Lead | Requirement 4: Maintain Auditable History, AuditLog Middleware, Automated Pytest Suite, UML Diagrams |

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, Django 5.x, Django REST Framework (DRF)
- **Frontend**: HTML5, Bootstrap 5.3, JavaScript (HTML5 WebCam QR Scanner)
- **Database**: PostgreSQL 16 (SQLite3 fallback)
- **Document Processing**: ReportLab (PDF), Pillow, qrcode
- **Testing**: Pytest, Django Test Framework
- **DevOps**: Docker, Docker Compose, GitHub Actions CI/CD, Vercel

---

## 🚀 Quick Execution Guide

```bash
# Clone the repository
git clone https://github.com/unclechipaz/qualification_verification_system.git
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
