# Requirements Traceability Matrix

## Midlands State University Qualification Verification System

| Document item | Value |
|---|---|
| Module | MIM736 – Software Engineering |
| Assignment | DevOps-Enabled Qualification Verification System Using Git and CI/CD Practices |
| Related specification | `docs/REQUIREMENTS.md`, version 0.2 |
| Matrix version | 0.2 – Updated baseline assessment |
| Baseline date | 10 September 2026 |
| Document owner | Project team |
| Approval status | Pending team review and project-lead approval |

## Document control

| Version | Date | Change | Prepared by | Approval |
|---|---|---|---|---|
| 0.1 | 9 September 2026 | Initial mapping of requirements to current implementation, tests and required evidence | Project team | Pending |
| 0.2 | 10 September 2026 | Updated implementation baseline, evidence and remaining work; retained requirement identifiers | Artwell (`artwel-dev`), with Codex assistance | Pending team review |

## Review baseline and interpretation

Reviewed on **10 September 2026** against `develop` at `77df668f0cb5a0e81118a63ce1439f36ca42cf8c` and the documentation in [PR #8](https://github.com/unclechipaz/qualification_verification_system/pull/8), head `ebc9594e49e17c40678f49c1d9e109753955e62b`. The application code is the same at these two revisions; PR #8 contains documentation changes and was **open, not merged**, when checked.

[PR #4](https://github.com/unclechipaz/qualification_verification_system/pull/4) repaired CI. [PR #6](https://github.com/unclechipaz/qualification_verification_system/pull/6) restricted public registration, applied password validation and checked login redirect destinations; it addresses [issue #5](https://github.com/unclechipaz/qualification_verification_system/issues/5). Both fixes are merged into `develop`. The [develop CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34408020848) and [PR #8 CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34471626306) completed successfully, including Django checks, migration-drift checking, pytest and Docker image building. These runs do not establish coverage, static analysis, PostgreSQL integration, deployment or complete security acceptance.

**Target versus current behaviour:** requirements, proposed controls and unchecked acceptance lists below describe work to deliver or approve. They are not claims of implementation or team sign-off. The assignment requires the four core capabilities, Git collaboration, CI/CD and quality evidence; detailed schema, role, hosting and numerical thresholds in this draft are proposed project decisions unless explicitly attributed to the brief. No additional assessment marks or lecturer requirements are inferred.

These findings apply to the inspected revisions. They do not establish the state of `main`, a live deployment or later commits. Refresh the evidence before release.

## 1. Purpose and use

This Requirements Traceability Matrix (RTM) connects every numbered requirement and core acceptance scenario in `docs/REQUIREMENTS.md` to:

- the current implementation evidence;
- available automated tests or other verification evidence;
- the current compliance status;
- the accountable team role; and
- the next evidence or corrective action required.

The team shall update this matrix in the same pull request that implements or materially changes a requirement. GitHub issue, pull-request, review and successful CI-run links shall replace `TBD` before final submission.

### 1.1 Status legend

| Code | Meaning |
|---|---|
| **I** | Implementation evidence is present. Passing release evidence may still be required. |
| **P** | Partially implemented, inconsistent or insufficiently verified. |
| **N** | Not implemented, contradicted by the baseline, or a material control is absent. |
| **E** | Engineering/process evidence must be produced through genuine GitHub or deployment activity. |
| **D** | A documented team or system-owner decision is required before implementation. |

### 1.2 Evidence rules

1. A source file proves only that code or configuration exists; it does not prove that the requirement passed.
2. A test-file reference proves only that a relevant test exists. A successful CI-run link is required as execution evidence.
3. A commit message without a corresponding file change is not accepted as implementation evidence.
4. Pull requests and reviews must be created through the genuine accounts of the people who performed and reviewed the work.
5. Screenshots should support, not replace, reproducible tests and GitHub links.
6. The failed runs reported on 7 September are historical. The [develop CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34408020848) and [PR #8 CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34471626306) now pass their configured checks. Record the exact run and scope; this is not evidence of the missing quality/deployment gates.

The documentation verification on 10 September recorded 13 passing local tests on Python 3.12.14/Django 5.1.15, using the code at `0faeb043c8c2c602008b1c7e1d45eb29efdcd098` (the same application code as the baseline above). Current CI targets Python 3.13. See Section 4 of `docs/TESTING_AND_VERIFICATION.md` for scope and limitations. Unless a row names local evidence, “no test” below means no corresponding committed automated test, not that no manual inspection ever occurred.

### 1.3 Baseline coverage summary

| Measure | Count |
|---|---:|
| SRS requirement and acceptance IDs traced | 139 of 139 |
| Implementation visible (**I**) | 23 |
| Partial or insufficiently verified (**P**) | 76 |
| Missing or contradicted (**N**) | 38 |
| Genuine engineering/process evidence pending (**E**) | 2 |
| Decision pending (**D**) | 0 |

These counts describe the inspected baseline and are not a percentage-completion calculation or a prediction of marks. Requirements have different risks and assessment importance.

## 2. Data-requirement traceability

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| DR-01 | `Student.student_number` is `unique=True` and indexed in `backend/students/models.py`. | No duplicate-number test. | **I** | Simba: add model/API duplicate test and CI link. |
| DR-02 | `Student.national_id` is unique and indexed, but is returned and displayed without adequate masking. | No uniqueness, masking or disclosure test. | **P** | Simba + Artwell: retain uniqueness, add masking and access tests. |
| DR-03 | `Certificate.student` is currently `OneToOneField`, preventing multiple certificates per student. | No multi-certificate test. | **N** | Simba: confirm target cardinality, migrate to one-to-many and test it. |
| DR-04 | `Qualification.code` is `unique=True` in `backend/qualifications/models.py`. | No duplicate-code test. | **I** | Simba: add constraint/API validation test. |
| DR-05 | Certificate number and verification code have database uniqueness constraints; verification code uses UUID generation. | No collision, null or concurrent-issuance test. | **I** | Simba: test generated identifiers and controlled collision handling. |
| DR-06 | No explicit database transaction protects a combined student/certificate issuance workflow. | No rollback/atomicity test. | **N** | Simba: implement `transaction.atomic()` around approved issuance flow. |
| DR-07 | Revocation reason is optional and the certificate does not store revoking actor/time. | No revocation-validation or attribution test. | **N** | Simba + Cleopatra: add fields/workflow, migration, validation and audit test. |
| DR-08 | Student and certificate have separate status fields without an enforced consistency rule. | No conflicting-status test. | **N** | Simba + Doreen: approve lifecycle and implement consistency validation. |
| DR-09 | Django uses `USE_TZ=True` and `TIME_ZONE='Africa/Harare'`; PDF output labels its timestamp as UTC. | No timezone-display test. | **P** | Charlton + Doreen: standardise storage/display and test expected timezone labels. |
| DR-10 | Docker Compose provides PostgreSQL, but Vercel configuration copies SQLite into temporary storage. | No persistence/redeployment test. | **P** | Charlton: move shared deployment to persistent PostgreSQL and demonstrate persistence. |
| DR-11 | The seed includes realistic/team-related identity values, known credentials, password resets on every run and two appended log rows per run. | Local fresh-seed counts confirmed; provenance of identity data is not established. | **N** | Simba + Cleopatra: replace with visibly synthetic values and a reviewed, idempotent demo seed. Do not assert the existing records belong to real people without evidence. |
| DR-12 | The legacy field is `digital_signature_hash`; it stores an unchecked SHA-256 digest. PR #8 explains the limitation; templates/PDF still overstate integrity. | Source inspection and local issuance check; no digest-reverification test. | **P** | Simba + Doreen: correct remaining UI/PDF claims and implement/check any approved integrity policy. |

## 3. Functional-requirement traceability

### 3.1 Identity and access management

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| FR-IAM-01 | Both web and API login try username, then email lookup; email is not unique, so duplicate-email login can error. | Username success/failure tests pass; email ambiguity is untested. | **P** | Charlton: test email login and agree a unique/normalised identity policy. |
| FR-IAM-02 | `logout_view()` calls Django logout and redirects to login. | No logout/session-invalidation test. | **I** | Charlton: add web integration test. |
| FR-IAM-03 | Web and API registration allow only EMPLOYER/PUBLIC_VERIFIER, defaulting to PUBLIC_VERIFIER, after PR #6. | Privileged-role rejection tests in `tests/test_authentication.py`; passing baseline CI linked above. | **I** | Charlton + Cleopatra: retain regression tests and extend to both privileged values on both routes. |
| FR-IAM-04 | `UserViewSet` uses `IsAdminOrRegistrar`, so a Registrar can currently modify user roles. | No role-management permission test. | **N** | Charlton: reserve privileged role changes for Administrator and test every role. |
| FR-IAM-05 | Several views/viewsets enforce role checks, but protection is inconsistent across record-list/detail paths. | No comprehensive permission matrix test. | **P** | Charlton + Cleopatra: parameterise tests for each role and endpoint. |
| FR-IAM-06 | `is_verified_employer` exists, but employer portal access checks only `role == 'EMPLOYER'`. | No verified/unverified-employer test. | **N** | Doreen + Charlton: enforce approval state server-side and test it. |
| FR-IAM-07 | Graduate dashboard uses `user.student_profile`, but `/qualifications/` and certificate-detail pages allow any logged-in user without ownership checks. | Local broad-access behaviour confirmed; no committed ownership regression test. | **P** | Doreen + Cleopatra: enforce ownership on list and detail routes, then test cross-account denial. |
| FR-IAM-08 | Login failure uses a generic invalid-credentials message. | API failure test exists; username-enumeration behaviour is not comprehensively tested. | **I** | Charlton: add unknown-email and disabled-account cases. |
| FR-IAM-09 | DRF static tokens are created, but no expiry, rotation or revocation workflow is present. | No token-lifecycle test. | **N** | Charlton: implement and document an approved token lifecycle. |
| FR-IAM-10 | Web login now validates `next` against the current request host and requires HTTPS when the request is secure. | External-destination rejection and local-redirect tests pass in `tests/test_authentication.py`. | **I** | Charlton: retain regressions; separately harden allowed hosts/proxy configuration and add edge cases. |

### 3.2 Register qualifications and certificates

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| FR-REG-01 | Qualification model and protected `QualificationViewSet` support CRUD; Django Admin is registered. | No qualification CRUD/permission tests. | **I** | Simba: add API validation and role tests. |
| FR-REG-02 | Student web form and protected `StudentViewSet` create records using current model fields. | No student-registration test. | **I** | Simba: add valid registration integration test. |
| FR-REG-03 | Database constraints reject duplicate identifiers; web code checks only duplicate student number and lacks full model-form validation. | No duplicate National ID, missing-field or invalid-date tests. | **P** | Simba: use validated forms/serializers and add negative tests. |
| FR-REG-04 | Certificate creation is available through protected API/Admin, but no dedicated controlled issuance UI/service exists. | No certificate-issuance test. | **P** | Simba: implement one approved issuance workflow and integration test. |
| FR-REG-05 | UUID verification codes are generated; certificate numbers use `Certificate.objects.count() + 1`, which is unsafe under concurrency. | No identifier-generation/concurrency test. | **P** | Simba: replace count-based generation and test collision handling. |
| FR-REG-06 | One-to-one certificate relationship prevents multiple awards per student. | No supporting test. | **N** | Simba: implement after DR-03 decision and migration. |
| FR-REG-07 | Certificate status defaults to `ACTIVE`. | No default-status test. | **I** | Simba: test default and explicitly permitted initial states. |
| FR-REG-08 | Protected certificate API/Admin can update status, but no purpose-built confirmation workflow exists. | No role/status-transition tests. | **P** | Simba + Doreen: implement controlled transition actions and tests. |
| FR-REG-09 | Revocation reason is optional and no confirmation rule is enforced. | No test. | **N** | Simba: validate mandatory reason for Revoked and add test. |
| FR-REG-10 | QR generation exists in `Certificate.qr_code_base64` and `backend/verification/utils.py`; one implementation hard-codes a deployment URL. | No QR payload or scan integration test. | **P** | Doreen + Charlton: use configured base URL and test safe payload. |
| FR-REG-11 | Audit middleware logs state-changing HTTP requests with path, user, IP and response status. | No audit-generation test; record-level detail is incomplete. | **P** | Cleopatra: implement domain audit events and test create/update/revoke. |
| FR-REG-12 | Student form says “Register Student & Issue Credential” but `student_create_view()` creates only a Student. | No complete workflow test. | **N** | Simba + Doreen: implement issuance or correct interface/manual wording. |

### 3.3 Search and retrieve qualification records

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| FR-SRCH-01 | Protected student list/API search student number, National ID and name; certificate API searches certificate/student identifiers. | `tests/test_verification.py` covers certificate and student-number lookup only. | **P** | Artwell: provide one coherent authorised search service covering all four fields. |
| FR-SRCH-02 | Current interfaces accept one general `q`/DRF `search` value and apply OR matching, not separate combinable filters. | No combined-filter test. | **N** | Artwell: add explicit filter parameters and defined AND behaviour. |
| FR-SRCH-03 | Verification service performs exact case-insensitive lookup for certificate, verification code, student number and National ID. | Tests cover certificate and student number only. | **P** | Artwell: add National-ID, verification-code, whitespace and case tests. |
| FR-SRCH-04 | `icontains` name matching exists, but public verification returns only `.first()`; protected student list returns a queryset. | No partial-name result-set test. | **P** | Artwell: return all authorised matches with pagination. |
| FR-SRCH-05 | `verify_qualification()` silently selects the first name match. | No duplicate-name test. | **N** | Artwell: implement ambiguity handling and test two identical/partial names. |
| FR-SRCH-06 | Serializers and verification responses disclose broad record details rather than role-minimised fields. | No field-level disclosure test. | **N** | Artwell + Charlton: define response serializers per role and test fields. |
| FR-SRCH-07 | Full National IDs appear in student tables, serializers, verification API and PDF output. | No masking test. | **N** | Artwell: implement reusable masking and assert raw National ID is absent. |
| FR-SRCH-08 | Anonymous verification currently accepts student number, National ID and name in addition to exact certificate identifiers. | No anonymous-search restriction test. | **N** | Artwell: restrict public lookup to certificate number/verification code. |
| FR-SRCH-09 | DRF global pagination is set to 20; HTML student list and some querysets are not paginated. | No pagination test. | **P** | Artwell: paginate all search result lists and test page boundaries. |
| FR-SRCH-10 | Key identifier/name fields have indexes; no representative query-plan evidence exists. | No performance dataset or `EXPLAIN` evidence. | **P** | Artwell + Simba: document query plans before/after indexes. |
| FR-SRCH-11 | Empty, spaces-only, non-string types, malformed payloads, and queries exceeding 150 characters are rejected with HTTP 400 (API) or friendly UI messages (web) in `backend/verification/views.py`. | Regression tests in `tests/test_verification.py` cover spaces-only, non-string, malformed body, and length boundaries. | **I** | Artwell: retain validation regressions and add throttling under FR-SRCH-12. |
| FR-SRCH-12 | Scoped DRF throttling is configured for public verification and API authentication. `APIVerifyView` uses the `api_verify` scope at 30 requests/minute and `APILoginView` uses the `api_login` scope at 5 requests/minute, with rates configured in `backend/msu_qvs/settings.py`. | Automated regression tests in `tests/test_verification.py` and `tests/test_authentication.py` confirm requests within the configured thresholds are processed and excess requests return HTTP 429. The complete local test suite passed (25 tests), Django system checks passed, and migration consistency reported no changes. | **I** | Artwell: retain rate-limit regressions and link Issue #13, the implementation PR, reviewer evidence and passing CI before final submission. |
| FR-SRCH-13 | Invalid public result is generally worded, but public routing still accepts restricted identifier types and stores raw queries. | No anti-enumeration test. | **P** | Artwell: standardise safe responses and compare restricted cases. |
| FR-SRCH-14 | Processed lookups create a VerificationLog with raw query text; blank web input and missing API query do not create one. | Local outcome/log checks exist; no committed query-masking test. | **P** | Artwell + Cleopatra: define attempted-versus-processed logging and protect restricted queries. |
| FR-SRCH-15 | Web and API call the same verification helper, but the helper implements insecure disclosure/search rules. | No web/API parity test. | **P** | Artwell: centralise approved policy and parameterise parity tests. |

### 3.4 Verify authenticity of qualifications

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| FR-VER-01 | `verify_qualification()` supports exact certificate number and verification code. | Certificate-number test exists; verification-code test is missing. | **I** | Doreen + Artwell: add code/QR path integration tests. |
| FR-VER-02 | Scanner page starts/stops camera preview and offers manual entry; no QR decoding or photo-upload handler is implemented. | Source inspection; no successful browser QR decoding evidence. | **P** | Doreen: implement decoder, supported URL/code parsing and browser tests; do not call camera preview a working scanner. |
| FR-VER-03 | Active certificates are mapped to `VERIFIED` in web and API views. | Existing test confirms record lookup, not rendered/API result and log. | **P** | Doreen: add full active-verification integration test. |
| FR-VER-04 | Revoked certificates are mapped to `REVOKED`. | Fraud-rule test covers a revoked certificate, not the verification response. | **P** | Doreen: test response, display and log status. |
| FR-VER-05 | API/log map SUSPENDED to PENDING; the web template falls through to the INVALID/not-found panel. | Local API/web mismatch reproduced; no committed suspended-status regression. | **P** | Doreen: fix the template and use one approved status mapping across UI/API/PDF. |
| FR-VER-06 | Missing records return `INVALID`; the service-level invalid lookup has a test. | No full public response/privacy/log integration test. | **P** | Doreen + Artwell: test safe response and created log. |
| FR-VER-07 | UI/API/PDF display certificate and student details, but output is not adequately minimised by role. | No content/disclosure test. | **P** | Doreen + Artwell: define public/employer/internal response schemas. |
| FR-VER-08 | Templates display text headings/icons as well as coloured status styling. | No accessibility/UI test. | **I** | Doreen + Cleopatra: add manual accessibility evidence and template test. |
| FR-VER-09 | ReportLab PDF generation and download route exist. | No PDF content or access-control test. | **P** | Doreen: test valid/revoked/invalid PDF content after securing route. |
| FR-VER-10 | PDF endpoint accepts a predictable numeric `log_id` and performs no ownership/role check. | No unauthorised-download test. | **N** | Doreen + Charlton: add object-level permission and negative tests. |
| FR-VER-11 | Digest is generated once but is not recalculated or verified during verification. | No digest-integrity test. | **N** | Simba + Doreen: implement verification or remove authenticity claim. |
| FR-VER-12 | Processed found/not-found lookups are logged; raw queries remain and no retention policy is implemented. | Local invalid response/log check; committed privacy/retention tests missing. | **P** | Cleopatra: retain invalid-outcome logging and add privacy/retention controls and tests. |

### 3.5 Auditable history

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| FR-AUD-01 | Web and API verification paths create `VerificationLog` records. | No audit integration test. | **I** | Cleopatra: add one log assertion for every verification outcome. |
| FR-AUD-02 | VerificationLog contains type, result, certificate, verifier, IP, user agent, risk fields and timestamp. | No completeness/privacy test. | **I** | Cleopatra: test mandatory fields and masked query storage. |
| FR-AUD-03 | Middleware logs POST, PUT, PATCH and DELETE requests but does not capture domain-level before/after change evidence. | No test. | **P** | Cleopatra: add explicit domain events for sensitive changes. |
| FR-AUD-04 | AuditLog contains actor, action, target, IP, details and timestamp; details contain only response status. | No field/content test. | **P** | Cleopatra: add outcome and safe before/after detail where required. |
| FR-AUD-05 | Ordinary users have no audit UI, but application-level immutability/deletion controls are not defined. | No tamper/delete permission test. | **P** | Cleopatra + Charlton: restrict deletion and test ordinary/admin behaviour. |
| FR-AUD-06 | Admin/Registrar dashboards and reports are role-protected, but complete audit-log access and scoping are not consistently documented. | No permission/report test. | **P** | Cleopatra: implement and test authorised audit review. |
| FR-AUD-07 | Employer portal and CSV export filter VerificationLog by `verified_by=request.user`. | No employer-isolation test. | **I** | Cleopatra: create two employers and prove cross-tenant isolation. |
| FR-AUD-08 | CSV exports raw query, IP and risk details; raw query may be a National ID. | No masking/export test. | **N** | Cleopatra + Artwell: minimise fields and add CSV privacy assertions. |
| FR-AUD-09 | No configurable retention or archival rule exists. | No retention test/evidence. | **N** | Cleopatra: obtain owner decision and document/test retention job. |
| FR-AUD-10 | Reports compute time-window and status summaries, but reproducible filters and boundary correctness are not proven. | No report-filter/count test; UTC/business-day and current-status versus logged-status questions remain. | **P** | Cleopatra: test Harare date boundaries and use recorded outcomes for historical reports. |
| FR-AUD-11 | Middleware does not store request bodies, but verification logs can store raw sensitive query values. | No secret/sensitive-log test. | **P** | Cleopatra: introduce sanitisation and test prohibited values. |
| FR-AUD-12 | Audit-write failure policy and monitoring are not implemented. | No failure-path test. | **N** | Cleopatra + Charlton: approve fail-safe behaviour and operational alert. |

### 3.6 Reports and supplementary monitoring

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| FR-RPT-01 | Daily, seven-day and thirty-day summaries exist; date boundaries need verification. Graduate total elsewhere compares GRADUATED with stored Graduated. | No committed deterministic summary test. | **P** | Cleopatra: correct case-sensitive counts and test timezone/window definitions. |
| FR-RPT-02 | CSV route permits Admin/Registrar and filters Employer exports to the current user. | No permission or isolation test. | **I** | Cleopatra: test all roles and two-employer isolation. |
| FR-RPT-03 | Report outputs do not consistently state generation time and selected criteria. | No output test. | **N** | Cleopatra + Doreen: add metadata to UI/CSV/PDF and test it. |
| FR-RPT-04 | All deterministic scoring rules and thresholds are documented in the PR #8 architecture guide; source still uses AI naming. | One revoked-certificate rule test passes; other boundaries untested. | **I** | Cleopatra: retain rule/limitation documentation and add boundary tests; treat scoring as advisory. |
| FR-RPT-05 | Scorer returns a flag/score/reason and does not directly change certificates or block accounts. | Existing revoked-rule test confirms scoring, not non-action across all rules. | **I** | Cleopatra: add tests confirming advisory-only behaviour. |
| FR-RPT-06 | PR #8 manuals clarify rule indicators; application AI/high-risk labels still need review. | Documentation inspection; no committed wording test. | **P** | Doreen + Cleopatra: correct any remaining labels that imply proof of fraud. |

## 4. Non-functional-requirement traceability

### 4.1 Security and privacy

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-SEC-01 | Registration privilege escalation is fixed; Registrar role administration, employer approval, public disclosure and object-access gaps remain. | Nine authentication tests; no full endpoint/object permission matrix. | **P** | Charlton + Cleopatra: test and correct the remaining permission paths. |
| NFR-SEC-02 | HTTPS may be supplied by hosting, but Django secure-cookie, redirect and HSTS settings are absent. | Previous deployment check reported failures; refresh after correction. | **N** | Charlton: add environment-controlled secure settings and evidence. |
| NFR-SEC-03 | Source contains fallback secret/database passwords and seed credentials. | No secrets scan in CI. | **N** | Charlton: remove production fallbacks, rotate exposed secrets and add scanning. |
| NFR-SEC-04 | Django CSRF middleware is enabled, but `ALLOWED_HOSTS` and CORS permit all origins/hosts. | No CSRF/CORS/host tests. | **P** | Charlton: restrict per environment and add configuration tests. |
| NFR-SEC-05 | Web/API registration call Django password validation and create hashed passwords; login password is write-only. | Web/API weak-password rejection tests pass; full response/log/password-change checks remain. | **I** | Charlton: retain password regressions and test response/log exclusion and future change flows. |
| NFR-SEC-06 | Some fields have browser requirements and ad-hoc checks, but server-side validation is incomplete. | No broad invalid-input suite. | **P** | All feature owners: use forms/serializers and add negative tests. |
| NFR-SEC-07 | No throttling classes/scopes are configured. | No 429 test. | **N** | Charlton + Artwell: add login/verification/search throttling. |
| NFR-SEC-08 | Public API/PDF can disclose full National ID and other details; logs retain raw query values. | No privacy test. | **N** | Artwell + Doreen + Cleopatra: minimise, mask and test all outputs. |
| NFR-SEC-09 | Current production settings do not satisfy Django deployment checks. | No successful hardened deployment-check artifact. | **N** | Charlton: run `manage.py check --deploy` in CI and attach result. |

### 4.2 Performance and scalability

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-PERF-01 | No performance test or two-second p95 result exists. | None. | **N** | Artwell: create representative exact-verification benchmark. |
| NFR-PERF-02 | No documented dataset size, concurrency or repeatable performance method exists. | None. | **N** | Artwell + Simba: define fixture size and record environment/results. |
| NFR-PERF-03 | DRF pagination is globally configured; HTML lists and selected reports remain unpaginated. | No pagination/load test. | **P** | Artwell: paginate search/list views and test boundaries. |
| NFR-PERF-04 | Indexes and several `select_related()` queries exist; no query-count or query-plan acceptance evidence exists. | None. | **P** | Artwell + Simba: add query-count tests and `EXPLAIN` evidence. |

### 4.3 Reliability and data consistency

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-REL-01 | No atomic end-to-end registration/issuance/revocation service exists. | No rollback test. | **N** | Simba: implement transactions and forced-failure tests. |
| NFR-REL-02 | PostgreSQL Docker volume is persistent, but public Vercel path uses temporary SQLite. | No redeployment persistence demonstration. | **P** | Charlton: deploy persistent database and test retained record. |
| NFR-REL-03 | Backup/restore procedure is now proposed in DEPLOYMENT_GUIDE.md; no completed restore exercise is evidenced. | Procedure only; execution record TBD. | **P** | Charlton + Simba: perform an isolated restore and record results before release. |
| NFR-REL-04 | Some expected errors are handled; duplicate National ID and other database/format errors may be unhandled. | Invalid lookup and login-failure tests cover limited cases. | **P** | All owners: add controlled 4xx/form-error tests. |
| NFR-REL-05 | Database uniqueness constraints exist, but automated constraint/relationship tests are incomplete. | Current tests create valid linked objects only. | **P** | Simba + Cleopatra: add duplicate, protected-delete and relation tests. |

### 4.4 Usability and accessibility

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-USE-01 | Home page provides a public verification form. | No first-time task/usability test. | **I** | Doreen: record a short acceptance test with a new user. |
| NFR-USE-02 | Templates provide messages and next steps, but terminology is inconsistent in some status/error paths. | No content review checklist. | **P** | Doreen: standardise terminology and capture review evidence. |
| NFR-USE-03 | Most forms use visible labels; complete keyboard/focus behaviour has not been verified. | No accessibility test. | **P** | Doreen + Cleopatra: perform keyboard and automated accessibility checks. |
| NFR-USE-04 | Bootstrap responsive layouts are used throughout templates. | No viewport evidence. | **I** | Doreen: attach mobile/tablet/desktop screenshots after deployment. |
| NFR-USE-05 | Status pages use text, icons and colour. | No accessibility regression test. | **I** | Doreen: verify contrast and screen-reader labels. |

### 4.5 Maintainability and portability

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-MNT-01 | Django apps separate authentication, students, qualifications, verification, employers, audit, reports and API. | Django system checks pass locally and in baseline CI. | **I** | Charlton: preserve boundaries as features and tests grow. |
| NFR-MNT-02 | No linter/static-analysis command runs. The display name is now Build & Test; the internal job ID remains test-and-lint. | No lint report. | **N** | Cleopatra + Charlton: add a reviewed linter and blocking CI command. |
| NFR-MNT-03 | Several environment values are configurable, but fallback secrets, hard-coded URLs and documentation variable mismatches remain. | No environment matrix test. | **P** | Charlton: centralise and document dev/test/production configuration. |
| NFR-MNT-04 | Migrations are committed and CI checks drift. The normal suite disables migrations; entrypoint still generates migrations at startup. | CI drift check passes; clean SQLite migration locally verified, PostgreSQL migration test absent. | **P** | Simba + Charlton: remove startup generation and add real PostgreSQL migration verification. |
| NFR-MNT-05 | PR #8 installation guide now uses the correct repository, isolated local database, variable names and test invocation. | Documented local install/check/seed workflows inspected and exercised; clean external workstation validation pending. | **P** | Charlton: retain PR #8 corrections and record a clean-machine run. |
| NFR-MNT-06 | Python 3.13 Docker image builds successfully in CI; Compose supplies PostgreSQL 16 and runserver. | Baseline CI Docker build succeeds; no container startup/PostgreSQL persistence evidence in this review. | **P** | Charlton: record Compose startup and database integration, then harden the release image. |

### 4.6 Testing and verification

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-TEST-01 | 13 tests: 9 authentication, 3 verification lookup and 1 rule test; registry, full search and audit coverage remain limited. | Existing suite passes locally; baseline CI pytest job succeeds. | **P** | Cleopatra coordinates requirement-specific tests from each feature owner. |
| NFR-TEST-02 | Negative registration/password/redirect cases were added in PR #6; broad duplicate, permissions and boundary coverage is still missing. | Six new security regression functions plus seven original functions. | **P** | Cleopatra: expand the catalogue into implemented tests without inflating test counts. |
| NFR-TEST-03 | Search tests do not cover all fields, combined filters, duplicates, masking, pagination or access. | Missing. | **N** | Artwell + Cleopatra: implement the full search acceptance suite. |
| NFR-TEST-04 | Pytest configuration has no coverage reporting or threshold. | Missing. | **N** | Cleopatra: add `pytest-cov`, report artifact and approved quality gate. |
| NFR-TEST-05 | Workflow does not run static analysis. | Missing. | **N** | Cleopatra + Charlton: add and enforce a static-analysis step. |
| NFR-TEST-06 | Tests create fixtures and pass in CI; some values use realistic institutional addresses and the seed still needs synthetic-data review. | Successful baseline CI plus local suite; not a certification of all demo-data provenance. | **P** | Cleopatra + Simba: use visibly fictional reserved examples consistently and retain clean-run evidence. |
| NFR-TEST-07 | This RTM now exists and provides stable requirement IDs, but GitHub/test/CI links remain to be populated. | Matrix coverage check required on every change. | **P** | Cleopatra: maintain completeness and link final evidence. |

### 4.7 DevOps and collaboration

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-DEV-01 | [issue #5](https://github.com/unclechipaz/qualification_verification_system/issues/5) records authentication remediation and is closed. Complete issue-to-requirement coverage for every member is not established. | [PR #6](https://github.com/unclechipaz/qualification_verification_system/pull/6) addresses issue #5. | **P** | Charlton: require traceable issues and acceptance criteria for remaining work. |
| NFR-DEV-02 | Focused CI, authentication and documentation branches now carry substantive changes; earlier generated-history branches remain historical. | [PR #4](https://github.com/unclechipaz/qualification_verification_system/pull/4), [PR #6](https://github.com/unclechipaz/qualification_verification_system/pull/6) and [PR #8](https://github.com/unclechipaz/qualification_verification_system/pull/8). | **P** | Every member: use the current integration baseline and link their own branch/issue. |
| NFR-DEV-03 | Recent CI/security/documentation commits contain file changes attributable to artwel-dev; historical no-tree-change commits remain unsuitable as proof of implementation. | PR #4, #6 and #8 diffs; whole-team contribution evidence incomplete. | **P** | Every member: report actual changed work, reviews and assistance truthfully; do not rely on commit totals. |
| NFR-DEV-04 | PR #4 and #6 were independently approved by cleonyabadza and merged by artwel-dev; PR #8 is open. | See EV-REVIEW-CI and EV-REVIEW-AUTH below. | **P** | All members: retain peer review for future changes; repository-wide enforcement/evidence remains to complete. |
| NFR-DEV-05 | Configured CI checks succeeded for recent merged fixes and PR #8. Missing gates and merge-rule enforcement still need work. | [develop CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34408020848); [PR #8 CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34471626306). | **P** | Charlton + Cleopatra: make agreed checks required and add missing quality gates. |
| NFR-DEV-06 | No defensible merge-conflict-resolution evidence was identified. | Conflict issue/PR/commit: `TBD`. | **E** | Charlton coordinates one genuine conflict and documents resolution. |
| NFR-DEV-07 | No release tag existed at assessment time. | Acceptance result and tag URL: `TBD`. | **E** | Charlton: tag only the tested, approved release. |
| NFR-DEV-08 | History generator remains in source; PR #8 CONTRIBUTING guide explicitly excludes its empty/generated commits from contribution evidence. | Documentation containment exists; whole-team acknowledgement/new-work evidence pending. | **P** | Charlton + all: do not run the generator or rewrite history to imply work; preserve truthful provenance. |
| NFR-DEV-09 | CI runs Django checks, drift check, pytest and Docker build; coverage, static analysis and controlled delivery are absent. | [develop CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34408020848) succeeds for the implemented stages. | **P** | Charlton + Cleopatra: add missing assessed stages and deployment evidence. |

### 4.8 Deployment and operations

| ID | Current implementation evidence | Existing verification evidence | Status | Owner and next action |
|---|---|---|:---:|---|
| NFR-OPS-01 | A public Vercel URL existed during assessment, but critical security/persistence/static-asset concerns remain. | Final approved deployment URL and smoke-test result: `TBD`. | **P** | Charlton: restrict unsafe baseline and redeploy corrected release. |
| NFR-OPS-02 | Docker supports PostgreSQL; Vercel uses temporary SQLite copying. | Persistence test: `TBD`. | **N** | Charlton: connect final deployment to persistent PostgreSQL. |
| NFR-OPS-03 | PR #8 installation guide and this deployment draft describe DJANGO_SECRET_KEY and individual DB_* variables; DATABASE_URL is not parsed. | Source/configuration comparison; actual hosting configuration unverified. | **P** | Charlton: reconcile the chosen deployment settings and document only implemented variables as current. |
| NFR-OPS-04 | A rollback/redeployment procedure is proposed in DEPLOYMENT_GUIDE.md; no completed exercise is evidenced. | Procedure only; run record TBD. | **P** | Charlton: perform a non-production rollback and retain evidence. |
| NFR-OPS-05 | Static CSS failure was observed in the 7 September assessment; this review did not re-test live assets. | Historical observation only; no current deployment asset evidence. | **P** | Charlton + Doreen: verify all required assets on the exact deployed release and resolve failures. |
| NFR-OPS-06 | No health endpoint exists; DEPLOYMENT_GUIDE.md proposes smoke checks, including an unimplemented /health/ call. | No deployed app/database health evidence. | **N** | Charlton: implement a safe health check or a working equivalent and record execution. |

## 5. Core acceptance-scenario traceability

| ID | Requirements covered | Current evidence | Status | Required acceptance evidence |
|---|---|---|:---:|---|
| AC-REG-01 | DR-03, DR-06, FR-REG-01 to FR-REG-11 | Separate models/API exist, but no complete transactional registration-and-issuance workflow/test. | **P** | Integration test, UI/API demonstration, audit assertion and successful CI link. |
| AC-REG-02 | DR-01, DR-02, FR-REG-03, NFR-REL-04 | Database uniqueness exists; validation and controlled-error handling are incomplete. | **P** | Duplicate student-number and National-ID tests proving no partial write. |
| AC-SRCH-01 | FR-SRCH-01 to FR-SRCH-04, FR-SRCH-06, FR-SRCH-09 | Single-value OR search exists; separate combined filters and minimisation do not. | **P** | API/UI test with two filters, authorised role, pagination and masked result. |
| AC-SRCH-02 | FR-SRCH-04, FR-SRCH-05 | Public helper returns first name match. | **N** | Fixture with duplicate/partial names and assertion that all authorised matches return. |
| AC-VER-01 | FR-VER-01, FR-VER-03, FR-VER-07, FR-VER-12 | Active lookup and status mapping exist; full response/log/privacy test is absent. | **P** | End-to-end UI/API verification and log assertion. |
| AC-VER-02 | FR-VER-04, FR-VER-07, FR-VER-12 | Revoked mapping and rule score exist; response/log test is absent. | **P** | Revoked certificate integration test and screenshot. |
| AC-VER-03 | FR-VER-06, FR-VER-12, FR-SRCH-13, FR-SRCH-14 | Invalid service result exists; privacy-safe response/log storage is incomplete. | **P** | Public invalid lookup test proving generic output and masked log. |
| AC-AUD-01 | FR-AUD-03 to FR-AUD-05 | Middleware records request metadata but not sufficient domain change evidence. | **P** | Status-change test asserting actor, target, outcome, before/after and timestamp. |
| AC-PERM-01 | FR-IAM-03 to FR-IAM-07, NFR-SEC-01 | Registration-role rejection is tested; Registrar role administration and object-access gaps remain. | **P** | Complete role/endpoint/object matrix and confirm denial without data changes. |

## 6. Assignment-deliverable traceability

| Assessed deliverable | Weight | Current evidence | Status | Evidence required before submission |
|---|---:|---|:---:|---|
| Git repository | 20% | Substantive fixes, independent reviews and successful CI are now evidenced by PR #4/#6; PR #8 adds corrected documentation. Historical generated activity is not proof of individual work. | **P** | Complete every member's issue/commit/review evidence, genuine conflict-resolution evidence and required gates. |
| Working software system | 25% | Django application and public deployment exist with material functional/security/persistence defects. | **P** | Corrected deployed release and functional acceptance record. |
| Technical report | 25% | Not assessed as part of the current repository baseline. | **E** | One 3,000–4,000-word team report covering every topic in the brief. |
| Demonstration and viva | 15% | Not yet evidenced. | **E** | 10–15-minute video covering system, Git, CI/CD, tests and verification. |
| Individual contribution reports | 15% | Genuine new role-specific evidence is not yet complete. | **E** | One report per member with linked issues, commits, PRs, reviews, tests and reflection. |

## 7. Prioritised corrective backlog

The following issue sequence addresses the highest marking and system risks first. Issue numbers and links shall be inserted after the team creates genuine GitHub issues.

| Priority | Proposed issue | Requirement IDs | Lead |
|---|---|---|---|
| P0 | Confirm and document the approved repository baseline | NFR-DEV-01 to NFR-DEV-08 | Charlton |
| P0 | Registration allowlist fixed in PR #6; separately restrict Registrar role management | FR-IAM-03, FR-IAM-04, NFR-SEC-01 | Charlton |
| P0 | Restrict anonymous search and remove public National-ID disclosure | FR-SRCH-06 to FR-SRCH-08, NFR-SEC-08 | Artwell |
| P0 | Secure PDF verification downloads | FR-VER-09, FR-VER-10 | Doreen |
| P0 | CI discovery/build fixed in PR #4; add coverage, static analysis and remaining requirement tests | NFR-TEST-01 to NFR-TEST-05, NFR-DEV-05, NFR-DEV-09 | Cleopatra + Charlton |
| P0 | Replace temporary production SQLite with persistent PostgreSQL | DR-10, NFR-REL-02, NFR-OPS-02 | Charlton |
| P1 | Implement complete, transactional certificate issuance | DR-03, DR-06, FR-REG-04 to FR-REG-06, FR-REG-12 | Simba |
| P1 | Implement authorised multi-parameter search and duplicate-name handling | FR-SRCH-01 to FR-SRCH-05 | Artwell |
| P1 | Strengthen and test domain-level audit trails | FR-AUD-03 to FR-AUD-12 | Cleopatra |
| P1 | Correct integrity-digest and rule-based anomaly terminology | DR-12, FR-VER-11, FR-RPT-04 to FR-RPT-06 | Simba + Doreen + Cleopatra |
| P1 | Harden deployment configuration and repair static assets | NFR-SEC-02 to NFR-SEC-04, NFR-SEC-09, NFR-OPS-03 to NFR-OPS-06 | Charlton |
| P2 | Complete accessibility, performance and operational evidence | NFR-PERF series, NFR-USE series, NFR-REL-03 | Assigned leads |

Additional dependency review: `Django>=5.0,<5.2` excludes currently supported releases; see SEC-RISK-020 in `SECURITY.md`. Plan and test an upgrade separately. This is not fixed by updating documentation.

## 8. Evidence register to complete

| Evidence reference | Description | Link/status |
|---|---|---|
| EV-ISSUE-REG | Registration and certificate-issuance issue | `TBD` |
| EV-ISSUE-SRCH | Search and retrieval issue | `TBD` |
| EV-ISSUE-VER | Verification and frontend issue | `TBD` |
| EV-ISSUE-AUD | Audit and QA issue | `TBD` |
| EV-ISSUE-DEV | CI/CD and deployment issue | `TBD` |
| EV-PR-REG | Simba's reviewed registration pull request | `TBD` |
| EV-PR-SRCH | Artwell's reviewed search pull request | `TBD` |
| EV-PR-VER | Doreen's reviewed verification pull request | `TBD` |
| EV-PR-AUD | Cleopatra's reviewed audit/testing pull request | `TBD` |
| EV-PR-DEV | Charlton's reviewed DevOps pull request | `TBD` |
| EV-CI-01 | Successful currently configured CI checks; not the complete target pipeline | [develop CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34408020848); [PR #8 CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34471626306) |
| EV-CD-01 | Successful controlled deployment | `TBD` |
| EV-TEST-01 | Test and coverage report | Existing suite and CI pass; coverage report and final requirement-verification report remain TBD. See testing-plan Section 4. |
| EV-STATIC-01 | Static-analysis report | `TBD` |
| EV-CONFLICT-01 | Genuine merge-conflict resolution | `TBD` |
| EV-UAT-01 | Team acceptance-test record | `TBD` |
| EV-RELEASE-01 | Approved final release tag | `TBD` |
| EV-VIDEO-01 | Demonstration video | `TBD` |
| EV-ISSUE-AUTH | Authentication security issue | [issue #5](https://github.com/unclechipaz/qualification_verification_system/issues/5); closed 9 September 2026 |
| EV-PR-CI-FIX | CI repair by artwel-dev, merged | [PR #4](https://github.com/unclechipaz/qualification_verification_system/pull/4) |
| EV-PR-AUTH-FIX | Authentication repair by artwel-dev, merged | [PR #6](https://github.com/unclechipaz/qualification_verification_system/pull/6) |
| EV-REVIEW-CI | Independent CI review by cleonyabadza | [Approval](https://github.com/unclechipaz/qualification_verification_system/pull/4#pullrequestreview-5159770205) |
| EV-REVIEW-AUTH | Independent security review by cleonyabadza | [Approval](https://github.com/unclechipaz/qualification_verification_system/pull/6#pullrequestreview-5160011050) |
| EV-PR-DOCS | Corrections to existing guides by artwel-dev; open when checked | [PR #8](https://github.com/unclechipaz/qualification_verification_system/pull/8) |

## 9. Maintenance and approval

### 9.1 Update procedure

For each requirement changed by a pull request, the author shall:

1. update the implementation evidence path;
2. add or update the automated test reference;
3. replace the status only when evidence supports the change;
4. add the issue, pull-request and successful CI-run links;
5. request review from the requirement owner and QA lead; and
6. confirm that related manuals and API documentation remain consistent.

### 9.2 Completion rule

The matrix is complete for release only when:

- every mandatory requirement has an implementation decision;
- every implemented requirement has reproducible verification evidence;
- every critical security and privacy requirement is compliant;
- all final CI checks pass;
- the deployed release matches the tested commit; and
- all `TBD` entries required for assessment evidence have been replaced.

### 9.3 Approval record

| Review role | Name | Decision | Date |
|---|---|---|---|
| Project Lead and DevOps Architect | Charlton | Pending | — |
| Database and Registry Lead | Simba | Pending | — |
| Search and Retrieval Specialist | Mncedisi (Artwell) | Pending | — |
| Verification and Frontend UI Specialist | Doreen | Pending | — |
| Audit Trail and QA Lead | Cleopatra | Pending | — |
