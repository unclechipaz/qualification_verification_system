# MSU QVS: Administrator Manual

**Source baseline:** `0faeb043c8c2c602008b1c7e1d45eb29efdcd098`, reviewed on 10 September 2026.

Use this manual with the [Installation Guide](INSTALLATION_GUIDE.md). The procedures describe the current application and its limitations; they are not a production-readiness certification.

## 1. Administrative access

Application pages and APIs generally use the `ADMINISTRATOR` or `REGISTRAR` role, with a superuser override. Django administration at `/admin/` separately requires an active staff account and appropriate model permissions, or a superuser.

To bootstrap your own administrator, run `python backend/manage.py createsuperuser` using the intended database and virtual environment, and complete its prompts. Assign the application's administrator role as appropriate in the user record. Demo accounts are described in the installation guide.

The seeded registrar is staff but receives no model permissions from `seed_db`. An administrator must grant the required permissions before that account can manage models through Django administration. Do not assume an application role automatically grants all Django-admin privileges.

Public registration now accepts only `EMPLOYER` and `PUBLIC_VERIFIER`, validates passwords and rejects privileged role selection. Administrators must provision graduate and staff accounts. Web login validates its `next` destination before redirecting; these authentication fixes do not resolve every other security issue in the system.

## 2. Register a student

1. Sign in at `/auth/login/` with administrator or registrar application access.
2. Open **Students**, then the add-student page at `/students/add/`.
3. Enter student number, national ID, full name, programme, faculty, level, graduation date, qualification text, degree classification and academic status.
4. Click **Save Student Record** and confirm the record appears in the student list.

This creates a `Student` only. It does not automatically create a `Qualification` definition, issue a `Certificate`, create a login account or link an existing user.

Student number and national ID must be unique. The web view explicitly checks duplicate student numbers, but does not consistently handle all other invalid inputs as friendly form errors. Check the data before saving and report unexpected errors.

## 3. Create qualification definitions and issue certificates

A qualification definition stores its title, unique code, faculty, department, duration and optional description. Manage it through Django administration with the necessary permissions, or through `/api/qualifications/`.

The `Student.qualification` text and the related `Certificate.qualification` record are separate. Keep them consistent.

For automatic certificate-number generation, use an authenticated administrator/registrar request to:

```http
POST /api/certificates/
Content-Type: application/json
Authorization: Token <YOUR_TOKEN>
```

Illustrative body; replace the IDs with existing records:

```json
{
  "student": 12,
  "qualification": 3,
  "issue_date": "2026-09-10",
  "status": "ACTIVE"
}
```

Confirm the response is `201 Created` and record its certificate number and verification code. See the [API reference](API_DOCUMENTATION.md) for authentication and field behaviour.

The API makes certificate number, verification code and digest read-only. The model generates them when appropriate. It allows one certificate per student. The generated numeric suffix uses the certificate count plus one, so numbering is not designed for concurrent issuance or arbitrary deletion/reuse.

Django's current add-certificate form treats certificate number as a required field. Supply an agreed unique number there, or use the API for automatic numbering. The **Qualifications Registry** web page provides listing and viewing, not an issue/revoke form.

QR PNG files are generated lazily when certain pages are viewed. Templates also generate Base64 QR images using a fixed Vercel URL. The SHA-256 field is a stored digest, not a digital signature or verification-time integrity check.

## 4. Revoke or suspend a certificate

1. Open the certificate in Django administration with change permission, or identify its API record ID.
2. Set the certificate's status to `REVOKED` or `SUSPENDED`.
3. Record the reason in `revocation_reason` and save.
4. Perform a new verification and check its recorded outcome.

The API equivalent is `PATCH /api/certificates/<id>/`, for example:

```json
{
  "status": "REVOKED",
  "revocation_reason": "Demonstration: withdrawn after registry review."
}
```

Changing `Student.status` alone does not revoke its certificate. Verification uses `Certificate.status`.

| Certificate status | New verification outcome |
| --- | --- |
| `ACTIVE` | `VERIFIED` |
| `REVOKED` | `REVOKED` |
| `SUSPENDED` | `PENDING` |

The web template does not yet render `PENDING` correctly; verify a suspended record through the API or the log. Changing status does not send an alert automatically. The heuristic detector evaluates the status on subsequent verification requests.

## 5. Graduate and employer accounts

Link a graduate's `Student.user` through Django administration so the graduate dashboard can find the correct profile. The student REST serializer does not expose that relationship. Only one student profile can be linked to a user.

Employer public registration creates a user with the employer role, but does not automatically create an `Employer` profile. Create that profile separately where needed. `User.is_verified_employer` and `Employer.is_verified_company` are separate flags; the employer portal currently checks role, not either approval flag.

The employer portal lists checks performed by the signed-in user. CSV export is also restricted to that employer's checks, while administrator/registrar exports cover all logs.

## 6. Reports and heuristic risk review

- `/reports/dashboard/`: role-directed dashboard.
- `/reports/analytics/`: administrator/registrar verification summaries.
- `/fraud/analytics/`: administrator/registrar heuristic risk summary.
- `/reports/export/csv/`: verification-log CSV export.

The detector scores revoked/suspended certificates, recent IP request counts, unmatched identifiers and selected user-agent strings. Scores are capped at 100; a score of 40 or more marks a request suspicious. It neither proves fraud nor blocks requests.

Some presentation/summary logic still needs correction: the administrator dashboard queries uppercase `GRADUATED` while the student model stores `Graduated`; active-result pages can label a high risk score “Safe”; and the revoked-attempt summary uses the certificate's current status. Validate important totals against the underlying records.

## 7. Audit records and preservation

`VerificationLog` records each processed verification search, its result, certificate, requesting user if known, IP, user agent, score, reason and timestamp. Blank web searches are not processed.

`AuditLogMiddleware` records POST, PUT, PATCH and DELETE requests, excluding static/media paths, with the user, path, IP and response status. It does not capture every GET, all field changes or a complete before/after record. Verification GET requests are recorded separately by the verification view.

Audit and verification records remain ordinary editable/deletable database records; there is no append-only storage, tamper-proof seal or automated retention policy. Do not promise an immutable audit trail.

Back up the configured database and required media. For SQLite, use a consistent database backup or stop writes before copying it; for PostgreSQL, use a database-aware backup procedure. Store backups with controlled access and test restoration into an isolated environment. The repository does not automate backups or restoration.

A PDF regenerated from a historical log uses the stored outcome and current certificate/student fields. Preserve an appropriately controlled snapshot if an evidential report must remain unchanged.

## 8. Access limits requiring code work

The registry and certificate-detail web views currently require login but do not restrict users to their own certificates. The verification API exposes student details, including national ID, publicly, and the PDF endpoint has no authentication or ownership check. Website logout does not revoke REST API tokens.

These behaviours are not corrected by documentation changes or by the public-registration fix. Use synthetic records while the team addresses and verifies the remaining controls. Follow the [deployment work list](INSTALLATION_GUIDE.md#deployment-status-and-remaining-work) before considering operational use.
