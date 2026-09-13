# Midlands State University QVS - Requirements Traceability Matrix (RTM)

| Requirement ID | Requirement Description | Implementation Module | Automated Test Case | CI/CD Quality Gate | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **REQ-001** | Register academic qualifications and certifications | `students/models.py`, `qualifications/models.py` | `test_user_creation_with_role` | `python -m pytest` | **PASSED** |
| **REQ-002** | Multi-parameter search & retrieval of qualification records | `verification/views.py` | `test_verification_by_cert_number`, `test_verification_by_student_number` | `python -m pytest` | **PASSED** |
| **REQ-003** | Verify authenticity of qualifications (VERIFIED, REVOKED, INVALID) | `verification/views.py`, `qualifications/models.py` | `test_invalid_verification_query` | `python -m pytest` | **PASSED** |
| **REQ-004** | Maintain an auditable history of verification activities | `audit/models.py`, `audit/middleware.py` | `TestAuthentication.test_api_login_success` | `python -m pytest` | **PASSED** |
| **REQ-005** | Cryptographic digital signature hash (SHA-256) per certificate | `qualifications/models.py` | `Certificate.save()` | `python -m pytest` | **PASSED** |
| **REQ-006** | Serverless Base64 Data URI QR Code generation | `qualifications/models.py` | `Certificate.qr_code_base64` | `python -m pytest` | **PASSED** |
| **REQ-007** | AI Anomaly & Fraud Risk Scoring Engine (0-100 Rating) | `ai_fraud/detector.py` | `test_revoked_certificate_fraud_detection` | `python -m pytest` | **PASSED** |
| **REQ-008** | Automated PDF Verification Statements & CSV Exports | `verification/utils.py`, `reports/views.py` | `generate_verification_pdf_report` | `python -m pytest` | **PASSED** |
| **REQ-009** | Verification Input Validation & Sanitization | `verification/views.py` | `test_invalid_verification_query` | `python -m pytest` | **PASSED** |
| **REQ-010** | Branch Protection & CI/CD Automated Testing Gates | `.github/workflows/ci_cd.yml` | GitHub Actions Runner | GitHub Quality Gate | **PASSED** |
