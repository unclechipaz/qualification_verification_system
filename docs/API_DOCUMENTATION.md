# Midlands State University QVS - REST API Documentation

Base URL: `http://localhost:8000/api/`

---

## 1. Authentication Endpoints

### POST `/api/login/`
Authenticates a user and returns a REST API Token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "AdminPass123!"
}
```

**Response (200 OK):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@msu.ac.zw",
    "role": "ADMINISTRATOR"
  },
  "status": "success"
}
```

---

## 2. Verification Endpoint

### POST `/api/verify/`
Public or authenticated endpoint to verify academic qualifications.

**Request Body:**
```json
{
  "query": "MSU-2024-BSC-CS-0001"
}
```

**Response (200 OK):**
```json
{
  "verification_id": 12,
  "query": "MSU-2024-BSC-CS-0001",
  "status": "VERIFIED",
  "timestamp": "2026-08-04T18:00:00Z",
  "ai_fraud_check": {
    "is_suspicious": false,
    "anomaly_score": 0,
    "reasons": "Normal Pattern"
  },
  "certificate_details": {
    "certificate_number": "MSU-2024-BSC-CS-0001",
    "verification_code": "VCODE-8F92-4A1C-99B0",
    "digital_signature_hash": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
    "student_name": "Artwell Zimba",
    "student_number": "R201452X",
    "national_id": "63-1234567-B-07",
    "programme": "BSc Computer Science",
    "faculty": "Science and Technology",
    "degree_classification": "First Class (1.1)",
    "graduation_date": "2024-11-20"
  }
}
```

---

## 3. Resource API ViewSets

| Endpoint | Method | Permission | Description |
| :--- | :--- | :--- | :--- |
| `/api/students/` | GET, POST | Admin / Registrar | List or register student records |
| `/api/qualifications/` | GET, POST | Admin / Registrar | Manage degree programs |
| `/api/certificates/` | GET, POST | Admin / Registrar | Manage issued certificates |
| `/api/employers/` | GET, POST | Admin / Registrar | Manage employer profiles |
| `/api/reports/` | GET | Admin / Registrar | Retrieve system analytics summary |
| `/api/fraud-analytics/` | GET | Admin / Registrar | Retrieve AI threat analytics |
