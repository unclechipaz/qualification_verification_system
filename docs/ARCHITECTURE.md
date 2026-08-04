# Midlands State University Qualification Verification System
## System Architecture Specification

### 1. High-Level Architecture Overview

The Midlands State University Qualification Verification System (MSU QVS) is built using a modern 3-Tier Architecture designed for security, scalability, high availability, and seamless third-party API integration.

```
+-------------------------------------------------------------------------+
|                              CLIENT LAYER                               |
|   +-------------------+    +--------------------+    +--------------+   |
|   |  Public Web UI    |    |   Employer Portal  |    |  QR Scanner  |   |
|   | (Bootstrap 5/HTML)|    | (screening history)|    |  (WebCam JS) |   |
|   +-------------------+    +--------------------+    +--------------+   |
+------------------------------------+------------------------------------+
                                     |
                                REST | HTTPS
                                     v
+------------------------------------+------------------------------------+
|                         APPLICATION SERVER (DJANGO)                     |
|  +------------------+  +-------------------+  +----------------------+  |
|  | Authentication   |  | Verification      |  | AI Fraud Anomaly     |  |
|  | & RBAC           |  | Engine            |  | Detector Engine      |  |
|  +------------------+  +-------------------+  +----------------------+  |
|  +------------------+  +-------------------+  +----------------------+  |
|  | Student & Cert   |  | PDF Generator     |  | Audit Log            |  |
|  | Management       |  | (ReportLab)       |  | Middleware           |  |
|  +------------------+  +-------------------+  +----------------------+  |
+------------------------------------+------------------------------------+
                                     |
                                ORM  | DB Driver
                                     v
+------------------------------------+------------------------------------+
|                          PERSISTENCE LAYER                              |
|   +------------------------------------------------------------------+  |
|   |  PostgreSQL 16 Database (Relational Store with Indexes)          |  |
|   +------------------------------------------------------------------+  |
+-------------------------------------------------------------------------+
```

---

### 2. Component Subsystems

1. **Authentication & RBAC**:
   - Manages custom users, hashed passwords, and token authentication.
   - Enforces role boundaries across 5 roles: `ADMINISTRATOR`, `REGISTRAR`, `GRADUATE`, `EMPLOYER`, `PUBLIC_VERIFIER`.

2. **Verification Engine**:
   - Executes multi-parameter search matching queries against Certificate Number, Student Number, Verification Code, National ID, or Full Name.
   - Computes SHA-256 cryptographic signatures to guarantee certificate authenticity.

3. **AI Fraud Detection Engine**:
   - Heuristic and rate anomaly evaluation computing an Anomaly Score (0 to 100).
   - Detects burst IP scanning, search attempts on revoked credentials, and suspicious automated agents.

4. **Document Generation Engine**:
   - Integrates ReportLab to produce dynamic, tamper-evident PDF verification reports and official printable degree certificates.
   - Integrates `qrcode` engine for generating high-density matrix barcodes.
