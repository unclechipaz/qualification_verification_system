# Changelog

## Unreleased - CI/CD delivery

- Add Ruff and 80% statement coverage gates, PostgreSQL migration/integration testing and retained quality artifacts.
- Add production Gunicorn/WhiteNoise container settings, health/revision endpoints, persistent Compose deployment and container recreation checks.
- Deliver the tested image to GHCR on successful develop/main push runs with commit/branch tags and a digest manifest.
- Upgrade to Django 5.2 LTS and pin runtime/developer dependencies; remove automatic migration generation and demo seeding from container startup.
- Add deployment and evidence instructions. These entries describe the proposed change; release execution and permanent deployment require their own evidence.

This file records significant project changes and their integration status.

## Unreleased
### feature/search-rate-limiting — Issue #13

- Implemented scoped DRF throttling for public verification and API authentication under FR-SRCH-12.
- Configured `api_verify` at 30 requests per minute and `api_login` at 5 requests per minute.
- Added automated regression tests confirming requests within the configured limits are processed and excess requests return HTTP 429 Too Many Requests.
- Confirmed the complete automated test suite passes with 25 tests.
- Confirmed Django system checks pass and no migration changes are required.

### feature/search-v2 — Issue #9

- Enforced consistent verification input validation across the REST API, web interface, and shared verification helper (`backend/verification/views.py`).
- Prevented false matches from empty or spaces-only queries by guarding against empty substring lookups and rejecting invalid queries before database execution.
- Added type validation rejecting non-string inputs (including booleans, numbers, lists, and objects) and malformed request bodies with controlled HTTP 400 responses.
- Implemented a 150-character query-length limit aligned with model constraints (`VerificationLog.search_query`).
- Preserved valid searches, alias parameters (`query`, `code`, `certificate_number`), and inputs with surrounding whitespace.
- Added comprehensive regression and boundary tests in `tests/test_verification.py`.

### Merged into develop — 9 September 2026

- Repaired automated test execution and updated CI workflow checks (PR #4).
- Restricted public registration to permitted roles, enforced password validation, and corrected unsafe login redirects (PR #6).

### Documentation under review — PR #8

- Updated the installation, API, user, administrator, architecture and contribution guides.
- Added requirements, requirements traceability, database ERD, testing, deployment and security documents.
- Corrected five README links to reference documents stored at the repository root.
