# MSU QVS: REST API Reference

**Source baseline:** `0faeb043c8c2c602008b1c7e1d45eb29efdcd098`, reviewed on 10 September 2026. Routes are defined in [backend/api/urls.py](../backend/api/urls.py).

Local base URL: `http://127.0.0.1:8000/api/`. All paths below include the `/api/` prefix and trailing slash. Examples use demonstration data.

## 1. Authentication and permissions

Send JSON bodies with `Content-Type: application/json`. Protected endpoints accept:

```http
Authorization: Token <TOKEN_RETURNED_BY_LOGIN_OR_REGISTRATION>
```

The application uses DRF database tokens, not JWTs. Session authentication is also configured; authenticated session requests that change data require a valid CSRF token. There is no implemented token refresh, token-expiry policy or API logout endpoint. Web logout does not delete an existing API token.

For the resource and analytics endpoints below, **administrator/registrar** means a signed-in user for whom `is_admin_or_registrar()` is true: role `ADMINISTRATOR`, role `REGISTRAR`, or a superuser. Employer and public-verifier tokens do not satisfy this permission.

### POST /api/login/

Accepts `username` and `password`. The username field can also contain an email address; a unique username is preferable because the model does not enforce email uniqueness.

```json
{
  "username": "employer1",
  "password": "EmployerPass123!"
}
```

On success, HTTP 200 returns `token`, `user` and `status: "success"`. The `user` object contains:

`id`, `username`, `email`, `first_name`, `last_name`, `role`, `national_id`, `phone_number`, `organization_name`, `is_verified_employer`, `created_at`.

Invalid credentials return HTTP 401:

```json
{"error": "Invalid Credentials"}
```

Missing/invalid input fields return HTTP 400 with serializer errors. The token and record IDs are generated values; do not copy a documentation sample as a real token.

### POST /api/register/

This public endpoint creates an employer or public-verifier user and returns HTTP 201 with the same `token`, `user`, `status` structure.

```json
{
  "username": "integration_demo",
  "email": "integration-demo@example.com",
  "password": "PineRiver!4826Lab",
  "role": "EMPLOYER",
  "organization_name": "Example Demonstration Company"
}
```

Use your own strong password when creating an actual account. Required fields are `username` and `password`. Optional fields are `email`, `first_name`, `last_name`, `role`, `national_id`, `phone_number` and `organization_name`. Omitted role defaults to `PUBLIC_VERIFIER`. The API does not use a `confirm_password` field.

Only `EMPLOYER` and `PUBLIC_VERIFIER` are permitted. Other roles, weak passwords, duplicate usernames and other serializer validation errors return HTTP 400. Password validation uses the configured Django validators.

Registration does not create an `Employer` profile, approve a company, issue a certificate or link a graduate record. Staff and graduate provisioning belongs to authorised administration.

## 2. Verification

### POST /api/verify/

This endpoint allows anonymous requests. Sending a valid token associates the resulting verification log with that user.

Submit a nonempty, trimmed string using `query`, `code` or `certificate_number`. If more than one is supplied, the code selects the first truthy value in that order.

```json
{"query": "MSU-2024-BSC-CS-0001"}
```

The lookup order is:

1. Exact certificate number, ignoring case.
2. Exact verification code, ignoring case.
3. Exact student number, ignoring case.
4. Exact national ID, ignoring case.
5. Partial student name, ignoring case.

The first certificate match is returned. There is no multiple-match selection, document upload, OCR or cryptographic signature validation. Whitespace-only and non-string inputs are not robustly validated; clients should validate their inputs.

| Condition | HTTP status | Body `status` |
| --- | --- | --- |
| Matching active certificate | 200 | `VERIFIED` |
| Matching revoked certificate | 200 | `REVOKED` |
| Matching suspended certificate | 200 | `PENDING` |
| No matching certificate | 404 | `INVALID` |
| No accepted input value | 400 | An `error` message instead of a verification result |

HTTP 200 alone does not mean a qualification is valid: inspect the body status.

Every processed verification result contains:

| Field | Content |
| --- | --- |
| `verification_id` | ID of the newly created log |
| `query` | Selected submitted value |
| `status` | Verification outcome |
| `timestamp` | ISO-formatted log timestamp |
| `ai_fraud_check.is_suspicious` | Boolean, true when score is at least 40 |
| `ai_fraud_check.anomaly_score` | Integer score from 0 to 100 |
| `ai_fraud_check.reasons` | Explanation string; `Normal Pattern` when there are no scoring reasons |

When a certificate matches, `certificate_details` is included for active, revoked and suspended records:

`certificate_number`, `verification_code`, `digital_signature_hash`, `student_name`, `student_number`, `national_id`, `programme`, `faculty`, `level`, `degree_classification`, `graduation_date`.

An invalid result omits `certificate_details`. Its fraud score may be nonzero because an unmatched identifier or the user-agent/frequency rules can add points.

The endpoint currently exposes these details, including national ID, without authentication. This is a privacy limitation requiring a code change. Use demonstration records. The digest is returned from storage; the endpoint does not recompute or validate it.

## 3. Resource endpoints

All five resources require administrator/registrar access.

| Collection | Purpose |
| --- | --- |
| `/api/users/` | User profile and role fields |
| `/api/students/` | Graduate/student registry records |
| `/api/qualifications/` | Qualification definitions |
| `/api/certificates/` | Issued certificates linked to student and qualification records |
| `/api/employers/` | Employer profiles linked to users |

Standard ModelViewSet operations are available:

| Path | Method | Successful response |
| --- | --- | --- |
| Collection | GET | 200, paginated list |
| Collection | POST | 201, created record |
| `<collection><id>/` | GET | 200, record |
| `<collection><id>/` | PUT or PATCH | 200, updated record |
| `<collection><id>/` | DELETE | 204, empty body |

Use PUT for full updates and PATCH for partial updates. Invalid serialized data generally returns 400; an unknown record returns 404. Missing/invalid token authentication normally returns 401, and an authenticated user without the required role returns 403. Database-level conflicts not handled by the view may produce server errors.

### Pagination and search

Lists use page-number pagination with 20 results per page:

```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

Request subsequent pages with `?page=2`. The search-enabled lists are:

- `/api/students/?search=R201452X`: student number, national ID, full name, programme.
- `/api/certificates/?search=MSU-2024-BSC-CS-0001`: certificate number, verification code, linked student number and linked full name.

The certificate list's search fields do not include national ID. Use the student list or the verification lookup for that field. The remaining resource viewsets do not configure search filters.

### Student fields

The serializer exposes `id`, `student_number`, `national_id`, `full_name`, `programme`, `faculty`, `level`, `graduation_date`, `qualification`, `degree_classification`, `status`, `created_at`, `updated_at`. ID and timestamps are read-only. `Student.user` is not exposed.

Dates use `YYYY-MM-DD`. Student statuses are case-sensitive: `Active`, `Graduated`, `Revoked`, `Suspended`. Student status does not automatically update certificate status, and creating a student does not issue a certificate.

### Qualification and certificate fields

Qualification records expose model fields including title, unique code, faculty, department, duration and description.

To issue a certificate, first create the student and qualification records, then POST their IDs:

```json
{
  "student": 12,
  "qualification": 3,
  "issue_date": "2026-09-10",
  "status": "ACTIVE"
}
```

The IDs above are illustrative. Certificate status choices are `ACTIVE`, `REVOKED` and `SUSPENDED`. `revocation_reason` and `qr_code_image` are also exposed. Nested `student_details` and `qualification_details` are read-only.

Certificate ID, certificate number, verification code, digest and creation timestamp are read-only. A student can have only one certificate. See the [Administrator Manual](ADMINISTRATOR_MANUAL.md) for numbering and status-change limitations.

### User and employer fields

`/api/users/` uses the user fields listed under login. It does not expose a password field or a password reset operation. Provision usable login accounts and manage their passwords through the appropriate registration/admin flow.

Employer records expose their model fields, including `user`, `company_name`, `industry`, `contact_person`, `contact_email`, `contact_phone` and `is_verified_company`. The current employer portal does not enforce company-approval flags.

## 4. Analytics

Both endpoints require administrator/registrar access.

### GET /api/reports/

Returns `total_students`, `total_certificates`, `active_certificates`, `revoked_certificates`, `total_verifications`, `verifications_today`, `verifications_this_week` and `suspicious_verifications`.

The “this week” calculation is a rolling seven-day interval. The “today” boundary is computed from `timezone.now()`; it should not be assumed to be a correctly localised Harare midnight.

### GET /api/fraud-analytics/

Returns `total_verifications`, `suspicious_count`, `suspicious_rate`, `revoked_attempts` and up to ten `high_risk_logs` with scores of at least 50.

Each high-risk log contains `id`, `search_query`, `anomaly_score`, `fraud_reason`, `ip_address` and `timestamp`. `revoked_attempts` uses the linked certificate's current status, so it is not a historical count based solely on the outcome recorded at verification time.

## 5. Related web downloads

These are web routes, not additional API routes:

| Route | Behaviour |
| --- | --- |
| `GET /verify/pdf/<log_id>/` | Generates a verification PDF; currently no login or ownership restriction |
| `GET /reports/export/csv/` | Session login required; employer receives own logs, administrator/registrar receives all logs |
| `GET /qualifications/certificate/<cert_number>/` | Session login required; printable HTML certificate without an ownership restriction |

The [Architecture](ARCHITECTURE.md) and [Administrator Manual](ADMINISTRATOR_MANUAL.md) describe the remaining integrity, audit and access-control limits.
