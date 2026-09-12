# Changelog

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
