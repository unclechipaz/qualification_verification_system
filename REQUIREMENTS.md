# Software Requirements Specification

## Midlands State University Qualification Verification System

| Document item | Value |
|---|---|
| Module | MIM736 – Software Engineering |
| Assignment | DevOps-Enabled Qualification Verification System Using Git and CI/CD Practices |
| Document version | 0.2 – Updated team-review draft |
| Date | 10 September 2026 |
| Document owner | Project team |
| Approval status | Pending team review and project-lead approval |

## Document control

| Version | Date | Change | Prepared by | Approval |
|---|---|---|---|---|
| 0.1 | 9 September 2026 | Initial requirements specification derived from the assignment and current repository baseline | Project team | Pending |
| 0.2 | 10 September 2026 | Updated implementation baseline, evidence and remaining work; retained requirement identifiers | Artwell (`artwel-dev`), with Codex assistance | Pending team review |

> **Requirements convention:** The word **shall** identifies a mandatory target requirement. A requirement in this document is not, by itself, evidence that the feature has already been implemented. Implementation and test evidence must be recorded in the Requirements Traceability Matrix.

## Review baseline and interpretation

Reviewed on **10 September 2026** against `develop` at `77df668f0cb5a0e81118a63ce1439f36ca42cf8c` and the documentation in [PR #8](https://github.com/unclechipaz/qualification_verification_system/pull/8), head `ebc9594e49e17c40678f49c1d9e109753955e62b`. The application code is the same at these two revisions; PR #8 contains documentation changes and was **open, not merged**, when checked.

[PR #4](https://github.com/unclechipaz/qualification_verification_system/pull/4) repaired CI. [PR #6](https://github.com/unclechipaz/qualification_verification_system/pull/6) restricted public registration, applied password validation and checked login redirect destinations; it addresses [issue #5](https://github.com/unclechipaz/qualification_verification_system/issues/5). Both fixes are merged into `develop`. The [develop CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34408020848) and [PR #8 CI run](https://github.com/unclechipaz/qualification_verification_system/actions/runs/34471626306) completed successfully, including Django checks, migration-drift checking, pytest and Docker image building. These runs do not establish coverage, static analysis, PostgreSQL integration, deployment or complete security acceptance.

**Target versus current behaviour:** requirements, proposed controls and unchecked acceptance lists below describe work to deliver or approve. They are not claims of implementation or team sign-off. The assignment requires the four core capabilities, Git collaboration, CI/CD and quality evidence; detailed schema, role, hosting and numerical thresholds in this draft are proposed project decisions unless explicitly attributed to the brief. No additional assessment marks or lecturer requirements are inferred.

These findings apply to the inspected revisions. They do not establish the state of `main`, a live deployment or later commits. Refresh the evidence before release.

## 1. Purpose

This Software Requirements Specification (SRS) defines the required behaviour, quality attributes, interfaces, data rules and acceptance conditions for the Midlands State University Qualification Verification System (MSU QVS).

The document has four purposes:

1. Translate the MIM736 practical-assignment brief into clear, testable requirements.
2. Give all five team members a common and controlled description of the system to be delivered.
3. Prevent the source code, tests, manuals, API documentation and demonstration from contradicting one another.
4. Provide stable requirement identifiers that can be linked to issues, commits, pull requests and automated tests.

## 2. Scope

### 2.1 Product objective

MSU QVS shall provide a secure and auditable way to register qualification records, search authorised records, verify the authenticity and current status of certificates, and preserve a history of verification and administrative activities.

### 2.2 In-scope capabilities

- Authentication and role-based access control.
- Registration and maintenance of students, qualifications and certificates.
- Search by certificate number, student number, National ID and student name for authorised users.
- Public verification through a certificate number, verification code or certificate QR code.
- Clear verification results for valid, revoked, suspended/pending and invalid credentials.
- Employer verification history and controlled reporting.
- Administrative and verification audit trails.
- REST API access for approved system functions.
- PDF verification statements and CSV exports subject to access control.
- Automated testing, continuous integration and continuous delivery evidence.
- Accessible deployment using Docker or an approved cloud platform, with persistent storage for shared use. A container plus managed database is the proposed project route; the assignment does not require both Docker and a cloud provider.

### 2.3 Out-of-scope capabilities

The following are outside the core assignment scope unless the team approves them as bonus work:

- Student admissions, course registration, examinations or fee management.
- Generation of full academic transcripts.
- Payments and billing.
- Blockchain credential storage.
- Integration with external universities or national identity databases.
- A trained machine-learning model or autonomous agentic AI system.
- Legal replacement of an original certificate or transcript.

The existing rule-based anomaly scorer may be retained as a supplementary security control, but it shall not be represented as agentic AI unless a genuine agentic capability is designed, implemented, tested and explained.

## 3. Assignment alignment

| Assignment requirement | SRS coverage | Primary evidence expected |
|---|---|---|
| Register qualifications or certifications | FR-REG series | Models, forms/API, validation tests and pull request |
| Search and retrieve qualification records | FR-SRCH series | Search service/API, database indexes and search tests |
| Verify authenticity of qualifications | FR-VER series | Verification portal/API, status tests and demonstration |
| Maintain an auditable history | FR-AUD series | Audit models, middleware/service tests and reports |
| Git collaboration | NFR-DEV series | Issues, branches, meaningful commits, pull requests and reviews |
| CI/CD and quality assurance | NFR-TEST and NFR-DEV series | Successful pipeline runs, coverage and static-analysis reports |
| Accessible deployment | NFR-OPS series | Deployment URL, configuration and deployment evidence |

## 4. Stakeholders and user roles

### 4.1 Stakeholders

| Stakeholder | Interest in the system |
|---|---|
| Midlands State University Registry | Accuracy and controlled maintenance of qualification records |
| Graduates | Correct presentation and verification of their own qualifications |
| Employers and other approved verifiers | Reliable verification of a candidate's qualification |
| Public verifiers | Limited confirmation that a presented certificate is valid |
| System administrators | User, role, configuration and operational administration |
| Project team | Design, implementation, testing, deployment and maintenance |
| Lecturer/assessor | Evidence of functionality, quality and genuine DevOps collaboration |

### 4.2 Application roles

The application shall use the following roles already represented by the custom `User` model:

- **Administrator:** manages users and roles and has authorised oversight of all system records.
- **Registrar:** registers and maintains students, qualifications and certificates.
- **Graduate:** views only the qualification records linked to their account.
- **Employer:** performs authorised candidate verification and views only its own screening history.
- **Public Verifier:** performs limited verification using an exact certificate identifier.

### 4.3 Role-access matrix

| Capability | Public verifier | Graduate | Employer | Registrar | Administrator |
|---|:---:|:---:|:---:|:---:|:---:|
| Exact public certificate verification | Yes | Yes | Yes | Yes | Yes |
| Search by National ID or student name | No | No | No by default | Yes | Yes |
| View full National ID | No | Own record only | No by default | Yes | Yes |
| View own certificate | No | Yes | No | Yes | Yes |
| View own verification history | No | No | Yes | Yes | Yes |
| Register students and qualifications | No | No | No | Yes | Yes |
| Issue, suspend or revoke certificates | No | No | No | Yes | Yes |
| Manage users and privileged roles | No | No | No | No | Yes |
| View complete audit and verification reports | No | No | No | Yes | Yes |

Access in this matrix is the target rule. Any broader access in the current baseline shall be treated as a defect rather than as an authorised feature.

## 5. System context and operating environment

### 5.1 Application architecture

The target solution shall use the repository's modular Django architecture:

- Python 3.13 application runtime, as configured in CI and Docker.
- Django web framework. The current dependency constraint is `Django>=5.0,<5.2`; a reviewed upgrade to a supported release is required before an internet-facing release (see `SECURITY.md`, SEC-RISK-020). This documentation revision does not change dependencies.
- Django REST Framework for API endpoints.
- PostgreSQL 16 for shared development, testing, staging and production deployments.
- SQLite for isolated local development or selected automated tests. SQLite can persist on a durable local filesystem; the repository's temporary serverless copy is the persistence problem.
- Bootstrap-based responsive web interface.
- Docker for repeatable deployment.
- GitHub and GitHub Actions for source control and CI/CD.

### 5.2 System boundary

The system receives user and API requests, applies authentication and authorisation rules, processes qualification data in a relational database, produces verification responses and reports, and writes audit evidence. Email delivery, external identity verification and external university integration are not part of the current boundary.

## 6. Data requirements

### 6.1 Core entities

| Entity | Purpose | Important attributes |
|---|---|---|
| User | Authentication and application role | Username, email, role, account status, organisation |
| Student | Graduate identity and academic record | Student number, National ID, full name, programme, faculty, level, graduation date, status |
| Qualification | Controlled qualification definition | Code, title, faculty, department, duration |
| Certificate | Issued credential linked to a student and qualification | Certificate number, verification code, issue date, status, QR reference, integrity digest |
| Employer | Verified organisation profile | Company, contact details, verification status |
| VerificationLog | Evidence of every verification attempt | Query type, result, certificate, verifier, time and source information |
| AuditLog | Evidence of security-relevant administrative activity | Actor, action, target, outcome, source and timestamp |

### 6.2 Data integrity rules

- **DR-01:** Every student number shall be present and unique.
- **DR-02:** Every National ID shall be present and unique for a student, but shall be treated as restricted personal data.
- **DR-03:** A student shall be able to hold one or more certificates; each certificate shall relate to exactly one student and one qualification.
- **DR-04:** Every qualification code shall be unique.
- **DR-05:** Every certificate number and verification code shall be unique and non-null.
- **DR-06:** Certificate creation shall be transactional so that partially created credentials are not retained after failure.
- **DR-07:** Revoked certificates shall include a revocation reason and the identity and time of the authorised action.
- **DR-08:** Certificate and student statuses shall follow a defined, consistent lifecycle; conflicting statuses shall not produce a valid result.
- **DR-09:** Timestamps shall be stored consistently and displayed using the Africa/Harare business timezone where appropriate.
- **DR-10:** Production and shared environments shall use persistent storage; temporary serverless SQLite storage shall not be used as the system of record.
- **DR-11:** Demonstration data shall be fictional and clearly labelled. Real student, employee or team-member personal data shall not be seeded into public environments.
- **DR-12:** A SHA-256 value calculated from record fields shall be described as an **integrity digest**, not a digital signature. A digital-signature claim requires asymmetric signing, protected private keys and signature verification.

### 6.3 Data classification and disclosure

| Data category | Examples | Default handling |
|---|---|---|
| Public verification data | Institution, qualification title, award status, issue year | May be disclosed only after an exact valid verification request |
| Restricted personal data | Full name, student number, National ID, contact details | Role-restricted; minimise and mask in responses and logs |
| Security-sensitive data | Passwords, tokens, secret keys, detailed audit records | Never expose in public responses, source code or screenshots |
| Operational data | Pipeline results, application metrics, deployment configuration | Restrict write access; publish only evidence appropriate for assessment |

## 7. Functional requirements

### 7.1 Identity and access management

- **FR-IAM-01:** The system shall authenticate a registered user using a username or registered email address and password.
- **FR-IAM-02:** The system shall provide a secure logout function that terminates the active session.
- **FR-IAM-03:** Self-registration shall permit only non-privileged roles approved by the team. A self-registering user shall not be able to select Administrator or Registrar. The current allowlist is `EMPLOYER` and `PUBLIC_VERIFIER`; Graduate and privileged accounts require authorised provisioning.
- **FR-IAM-04:** Only an Administrator shall assign or change privileged roles.
- **FR-IAM-05:** Every protected web view and API endpoint shall enforce server-side role permissions; hiding a menu item shall not be considered access control.
- **FR-IAM-06:** An Employer shall not receive employer-only privileges until its organisation has been verified and approved.
- **FR-IAM-07:** A Graduate shall access only the student and certificate records linked to that graduate's account.
- **FR-IAM-08:** Authentication failures shall return a generic message that does not reveal whether a username or email address exists.
- **FR-IAM-09:** API credentials or tokens shall be revocable and shall follow an approved expiry or rotation policy.
- **FR-IAM-10:** Redirection after login shall be restricted to safe local destinations.

### 7.2 Register qualifications and certificates

- **FR-REG-01:** An Administrator or Registrar shall create and maintain a qualification containing a unique code, title, faculty, department, duration and optional description.
- **FR-REG-02:** An Administrator or Registrar shall register a student using the mandatory fields defined by the `Student` model.
- **FR-REG-03:** The system shall reject duplicate student numbers, duplicate National IDs and invalid or incomplete mandatory fields with understandable validation messages.
- **FR-REG-04:** An Administrator or Registrar shall issue a certificate by selecting an existing student and qualification and supplying an issue date.
- **FR-REG-05:** Certificate issuance shall generate a collision-resistant certificate number and an unpredictable verification code.
- **FR-REG-06:** The system shall support more than one qualification or certificate for a student without duplicating the student's identity record.
- **FR-REG-07:** The initial certificate status shall be explicitly selected or default to Active according to the approved registry workflow.
- **FR-REG-08:** Only an Administrator or Registrar shall change a certificate to Suspended or Revoked.
- **FR-REG-09:** Revocation shall require a reason and confirmation before the change is saved.
- **FR-REG-10:** The system shall generate a QR code containing a verification URL or verification code; the QR code shall not contain a National ID or other unnecessary personal data.
- **FR-REG-11:** Create, update, suspend and revoke operations shall generate an audit event.
- **FR-REG-12:** The user interface and manuals shall not state that saving a student automatically issues a certificate unless the application performs and tests that complete transaction.

### 7.3 Search and retrieve qualification records

- **FR-SRCH-01:** An authorised Registrar or Administrator shall search qualification records by certificate number, student number, National ID and student name.
- **FR-SRCH-02:** The internal search interface and API shall accept one or more separate search parameters and combine supplied filters consistently.
- **FR-SRCH-03:** Certificate number, student number, National ID and verification-code searches shall support normalised exact matching.
- **FR-SRCH-04:** Name search shall support case-insensitive partial matching and return every authorised match, subject to pagination.
- **FR-SRCH-05:** When a name or partial value matches more than one record, the system shall return a result list; it shall not silently select the first record.
- **FR-SRCH-06:** Search results shall show only fields required for the user's authorised purpose.
- **FR-SRCH-07:** National IDs shall be masked in ordinary result lists and shall never be exposed to anonymous users.
- **FR-SRCH-08:** Anonymous public verification shall accept only an exact certificate number or unpredictable verification code, including a code obtained from a QR scan.
- **FR-SRCH-09:** Search results exposed through list APIs shall be paginated. The initial repository configuration uses 20 records per page.
- **FR-SRCH-10:** Frequently searched identifiers shall have appropriate database indexes and query plans shall be reviewed using a representative dataset.
- **FR-SRCH-11:** Empty, excessively long and malformed search inputs shall be rejected without causing a server error.
- **FR-SRCH-12:** Public verification and authentication requests shall be rate-limited to reduce enumeration and automated abuse.
- **FR-SRCH-13:** A public invalid-result response shall not confirm whether a National ID, student account or other restricted identifier exists.
- **FR-SRCH-14:** Every completed verification search shall create a VerificationLog record using a safely stored or masked query value.
- **FR-SRCH-15:** The web interface and REST API shall apply the same search, disclosure and authorisation rules.

### 7.4 Verify authenticity of qualifications

- **FR-VER-01:** The system shall verify a certificate using an exact certificate number or unpredictable verification code.
- **FR-VER-02:** The QR scanning interface shall extract a supported verification URL/code and submit it to the normal verification service.
- **FR-VER-03:** A matching Active certificate with consistent linked records shall return **VERIFIED**.
- **FR-VER-04:** A matching Revoked certificate shall return **REVOKED** and shall not be presented as valid.
- **FR-VER-05:** A matching Suspended certificate shall return **SUSPENDED** or **PENDING**, according to one approved term used consistently throughout the code and documentation.
- **FR-VER-06:** No matching certificate shall return **INVALID/NOT FOUND** without disclosing private registry information.
- **FR-VER-07:** A verification result shall include the certificate number, qualification title, institution, status and verification timestamp. Additional personal data shall be minimised according to role.
- **FR-VER-08:** A verification result shall display status using both text and visual styling; colour alone shall not communicate the result.
- **FR-VER-09:** The system shall provide an authorised, printable PDF verification statement whose content matches the on-screen result.
- **FR-VER-10:** A PDF download shall verify that the requester is authorised for the underlying verification record; a predictable log identifier alone shall not grant access.
- **FR-VER-11:** If an integrity digest is used, the system shall define the protected fields and shall verify the digest before claiming that the record is unchanged.
- **FR-VER-12:** A verification request and its result shall be recorded even when no certificate is found, subject to privacy and log-retention controls.

### 7.5 Auditable history

- **FR-AUD-01:** The system shall record every certificate-verification attempt in `VerificationLog`.
- **FR-AUD-02:** The verification log shall record the search type, result, related certificate where found, authenticated verifier where applicable, timestamp and necessary source information.
- **FR-AUD-03:** The system shall record security-relevant data changes, including creation, modification, suspension, revocation and deletion attempts.
- **FR-AUD-04:** An administrative audit record shall include actor, action, target, outcome, timestamp and source address. Where appropriate, it shall record safe before-and-after values.
- **FR-AUD-05:** Audit records shall be protected against alteration or deletion by ordinary application users.
- **FR-AUD-06:** Only authorised Registrar and Administrator roles shall view complete audit and verification histories.
- **FR-AUD-07:** An Employer shall view and export only verification records created by that employer account.
- **FR-AUD-08:** Audit and CSV exports shall mask or omit restricted identifiers unless the recipient has an approved need to view them.
- **FR-AUD-09:** Audit retention shall be configurable and documented. Records shall not be silently discarded.
- **FR-AUD-10:** Reporting shall provide at least verification totals by period and status, with filters that can be reproduced and tested.
- **FR-AUD-11:** Audit logging shall avoid storing passwords, authentication tokens, secret keys or unnecessary form contents.
- **FR-AUD-12:** Failure to write an essential audit record shall be detected and handled according to an approved error policy.

### 7.6 Reports and supplementary monitoring

- **FR-RPT-01:** An authorised Registrar or Administrator shall view daily, seven-day and thirty-day verification summaries.
- **FR-RPT-02:** An authorised user shall export only the verification history permitted by that user's role.
- **FR-RPT-03:** Reports shall display the criteria and generation timestamp so that results can be interpreted correctly.
- **FR-RPT-04:** If rule-based anomaly scoring is retained, the system shall document each rule, threshold and limitation.
- **FR-RPT-05:** The rule-based anomaly scorer shall not independently revoke a certificate, block a user or take another material action without an authorised workflow.
- **FR-RPT-06:** Rule-based anomaly results shall be described as indicators requiring review, not proof of fraud.

## 8. External interface requirements

### 8.1 Web interface

- The web interface shall be usable on common desktop and mobile screen sizes.
- Forms shall have visible labels, mandatory-field indicators and clear validation messages.
- Protected navigation and pages shall be consistent with the role-access matrix.
- Status pages shall not expose full National IDs, private contact information, tokens or internal audit details to public users.

### 8.2 REST API

- API requests and responses shall use JSON except for documented file downloads.
- Protected endpoints shall require an authenticated session or API token and the correct role.
- Validation failures shall return an appropriate 4xx status and structured error information.
- Server failures shall return a generic error without a debug traceback or secret configuration.
- API search and verification behaviour shall match the corresponding web behaviour.
- API endpoints and example payloads shall be maintained in `docs/API_DOCUMENTATION.md`.

### 8.3 QR and camera interface

- The QR scanner shall request browser camera permission only after user action.
- Manual entry shall remain available when camera access is unavailable.
- Scanned content shall be validated before navigation or submission.

### 8.4 Report interfaces

- PDF output shall be readable, printable and clearly identified as a verification statement rather than an original certificate.
- CSV exports shall use consistent headings, safe character encoding and access-controlled data fields.

## 9. Non-functional requirements

### 9.1 Security and privacy

- **NFR-SEC-01:** The system shall apply least-privilege role-based access control to every protected operation.
- **NFR-SEC-02:** Production traffic shall use HTTPS, secure cookies and appropriate transport-security settings.
- **NFR-SEC-03:** Secret keys, database passwords and tokens shall be supplied through protected environment configuration and shall not use insecure source-code fallbacks in production.
- **NFR-SEC-04:** The application shall use CSRF protection for state-changing browser requests and shall restrict permitted origins and hosts.
- **NFR-SEC-05:** Passwords shall be processed through Django's password hashing and validation mechanisms and shall never be logged or returned by an API.
- **NFR-SEC-06:** Inputs shall be validated on the server, regardless of browser-side validation.
- **NFR-SEC-07:** Public and sensitive endpoints shall use throttling appropriate to the test environment.
- **NFR-SEC-08:** Personal data shall be collected, displayed, logged and retained only to the extent required for the verification purpose.
- **NFR-SEC-09:** Production configuration shall pass Django's deployment security checks or document an approved exception.

### 9.2 Performance and scalability

- **NFR-PERF-01:** Exact certificate verification shall complete within two seconds for at least 95% of requests in the agreed staging performance test.
- **NFR-PERF-02:** The performance-test dataset size and concurrency shall be recorded with the result so the measurement is reproducible.
- **NFR-PERF-03:** List and search endpoints shall use pagination and shall not load the complete registry into one response.
- **NFR-PERF-04:** Database access shall avoid unnecessary repeated queries and shall use indexes for approved search fields.

### 9.3 Reliability and data consistency

- **NFR-REL-01:** A failed registration, issuance or revocation transaction shall not leave a partially updated credential.
- **NFR-REL-02:** The production database shall persist across application restarts and redeployments.
- **NFR-REL-03:** A documented backup and restore test shall be completed before final release.
- **NFR-REL-04:** Expected invalid input shall produce a controlled response rather than an unhandled server error.
- **NFR-REL-05:** Database uniqueness and relationship constraints shall be verified through automated tests.

### 9.4 Usability and accessibility

- **NFR-USE-01:** A first-time verifier shall be able to submit an exact certificate verification from the home page without training.
- **NFR-USE-02:** Error and status messages shall use plain language and provide a safe next step.
- **NFR-USE-03:** Interactive controls shall be keyboard accessible and associated with visible labels.
- **NFR-USE-04:** Text and interface controls shall remain legible at common mobile and desktop widths.
- **NFR-USE-05:** The application shall not rely on colour alone to distinguish Verified, Revoked, Pending/Suspended and Invalid results.

### 9.5 Maintainability and portability

- **NFR-MNT-01:** The application shall retain clear Django modules for authentication, students, qualifications, verification, employers, audit and reports.
- **NFR-MNT-02:** Source code shall follow an agreed Python coding standard and pass the configured static-analysis checks.
- **NFR-MNT-03:** Environment-specific values shall be read from configuration rather than being duplicated in code and documentation.
- **NFR-MNT-04:** Database migrations shall be version controlled and reproducible on a clean database.
- **NFR-MNT-05:** A new developer shall be able to install and run the system using the maintained installation guide.
- **NFR-MNT-06:** Docker configuration shall provide a reproducible application and PostgreSQL environment.

### 9.6 Testing and verification

- **NFR-TEST-01:** Core registration, search, verification, permissions and audit requirements shall have automated unit or integration tests.
- **NFR-TEST-02:** Tests shall include successful, invalid, duplicate, unauthorised and boundary cases.
- **NFR-TEST-03:** Search tests shall cover every supported parameter, combined filters, duplicate names, case handling, pagination, masking and unauthorised access.
- **NFR-TEST-04:** The pipeline shall generate a test-coverage report and enforce the coverage threshold approved by the team before release.
- **NFR-TEST-05:** The pipeline shall perform static analysis and fail when an agreed blocking issue is detected.
- **NFR-TEST-06:** Tests shall use fictional deterministic data and shall run successfully on a clean checkout.
- **NFR-TEST-07:** Requirement-to-test evidence shall be maintained in `docs/REQUIREMENTS_TRACEABILITY_MATRIX.md`.

### 9.7 DevOps and collaboration

- **NFR-DEV-01:** Every unit of assigned work shall begin with a traceable GitHub issue containing acceptance criteria.
- **NFR-DEV-02:** New work shall be performed on a focused branch created from the approved integration baseline.
- **NFR-DEV-03:** Every commit shall contain the actual change described by its message and preserve the real author's identity.
- **NFR-DEV-04:** Features shall enter `develop` through a pull request reviewed by a team member other than the author.
- **NFR-DEV-05:** Required CI tests and quality checks shall pass before merge.
- **NFR-DEV-06:** The team shall retain evidence of at least one genuinely resolved merge conflict.
- **NFR-DEV-07:** Release candidates shall be merged into `main` only after acceptance testing and shall receive an approved release tag.
- **NFR-DEV-08:** Automated empty commits or generated history shall not be used as evidence of individual contribution.
- **NFR-DEV-09:** The pipeline shall automate build, test and quality checks and shall provide a controlled continuous-delivery stage for the approved deployment environment.

### 9.8 Deployment and operations

- **NFR-OPS-01:** The system shall be deployed to an environment accessible to the assessor during the agreed assessment period.
- **NFR-OPS-02:** The deployment shall use a persistent database suitable for shared access.
- **NFR-OPS-03:** Deployment instructions shall identify required environment variables without publishing their secret values.
- **NFR-OPS-04:** The team shall document and demonstrate a safe rollback or redeployment procedure.
- **NFR-OPS-05:** Static and media assets required by the demonstrated functionality shall load successfully in the deployed environment.
- **NFR-OPS-06:** A health check or equivalent repeatable verification shall confirm that the deployed application and database are available.

## 10. Core acceptance scenarios

### AC-REG-01: Register and issue a qualification certificate

**Given** an authenticated Registrar and valid, non-duplicate student and qualification information,  
**when** the Registrar saves the student and issues a certificate,  
**then** the linked records are stored, unique identifiers are generated, the operation is audited and the certificate can be retrieved.

### AC-REG-02: Reject a duplicate identity

**Given** a student number or National ID already exists,  
**when** a Registrar submits another student using that identifier,  
**then** the system rejects the request, explains the conflict and creates no partial record.

### AC-SRCH-01: Authorised multi-parameter search

**Given** an authenticated Registrar,  
**when** one or more supported search parameters are submitted,  
**then** all matching authorised records are returned in a paginated result with restricted fields handled according to the role.

### AC-SRCH-02: Duplicate-name handling

**Given** two or more students share a full or partial name,  
**when** an authorised user searches that name,  
**then** the system returns the matching result set and does not silently choose one certificate.

### AC-VER-01: Verify an active certificate

**Given** an Active certificate with consistent linked records,  
**when** its exact certificate number or verification code is submitted,  
**then** the system returns VERIFIED, displays minimised qualification information and creates a verification log.

### AC-VER-02: Handle a revoked certificate

**Given** a Revoked certificate,  
**when** its exact identifier is submitted,  
**then** the system returns REVOKED, does not describe it as valid and records the attempt.

### AC-VER-03: Handle an invalid identifier safely

**Given** an identifier that matches no certificate,  
**when** a public verifier submits it,  
**then** the system returns INVALID/NOT FOUND without confirming the existence of a student or National ID and records a privacy-safe log entry.

### AC-AUD-01: Preserve administrative evidence

**Given** an authenticated Registrar changes a certificate's status,  
**when** the change succeeds or fails,  
**then** the system records the actor, action, target, outcome, time and safe source information in a protected audit record.

### AC-PERM-01: Reject an unauthorised operation

**Given** a public, graduate or employer account,  
**when** it attempts to create a student, change a certificate or retrieve restricted registry data,  
**then** the system returns an access-denied response and makes no data change.

## 11. Current-baseline deviations requiring correction

This section keeps the specification compatible with the current repository without misrepresenting incomplete behaviour as compliant.

| Target requirement | Current baseline observation | Required action |
|---|---|---|
| FR-IAM-03 and FR-IAM-04 | Public web/API registration now rejects privileged roles after PR #6. `UserViewSet` still permits Registrar access to user-role updates. | Retain registration regression tests; separately restrict privileged-role management to Administrators (TC-IAM-006). |
| FR-SRCH-07 and FR-SRCH-08 | Anonymous verification can search National ID/name and responses may disclose full National ID | Separate public exact verification from authorised internal search and minimise results |
| FR-SRCH-04 and FR-SRCH-05 | Name verification returns only the first matching certificate | Return an authorised result list or require a unique exact identifier |
| DR-03 and FR-REG-06 | `Certificate.student` still uses a one-to-one relationship; the SRS proposes multiple certificates. | Approve the target cardinality, then migrate and update every affected form, serializer, reverse relation and test. Do not describe the proposed relationship as implemented. |
| FR-REG-12 | The student form states that it issues a credential but creates only a Student record | Implement a complete issuance workflow or correct the interface wording |
| FR-VER-10 | Verification PDFs are retrieved using a predictable numeric log identifier without an ownership check | Add object-level authorisation or a secure unguessable download mechanism |
| DR-12 and FR-VER-11 | A stored SHA-256 digest is described as a digital signature/tamper-evident proof without verification | Correct the terminology or implement genuine signing and verification |
| FR-RPT-04 to FR-RPT-06 | The scorer uses fixed rules. PR #8 documents these limits, but application labels still say AI fraud. | Retain accurate documentation and correct any UI claims that imply machine learning or proof of fraud. |
| NFR-SEC-02 to NFR-SEC-09 | Wildcard hosts/origins, insecure fallback settings and missing throttling remain | Harden production configuration and add security tests |
| NFR-OPS-02 | Serverless deployment relies on temporary SQLite copying | Use persistent PostgreSQL or another approved persistent service |
| NFR-TEST-03 to NFR-TEST-05 | CI now succeeds for 13 test functions, Django checks, migration-drift checking and Docker build. Coverage, static analysis and the full search suite are absent. | Expand requirement tests and add the missing quality gates; retain links to successful runs. |

Additional current gaps: the API returns `PENDING` for a suspended certificate while the web page falls through to its invalid-result panel; the camera page starts a preview but has no QR decoder or image-upload handler; and the default protected-page redirect points to the missing `/accounts/login/` route. These remain implementation tasks under FR-VER-02, FR-VER-05, FR-IAM-05 and NFR-USE-02.

## 12. Requirement ownership

Ownership identifies the member accountable for coordinating the requirement; it does not prevent peer review or shared implementation.

| Requirement group | Accountable role/member | Required peer involvement |
|---|---|---|
| Architecture, DevOps and deployment | Charlton – Project Lead and DevOps Architect | All members provide pipeline and deployment evidence |
| FR-REG and core data rules | Simba – Database and Registry Lead | Charlton reviews migration/deployment impact |
| FR-SRCH | Mncedisi (Artwell) – Search and Retrieval Specialist | Cleopatra reviews tests; Simba reviews indexes/data rules |
| FR-VER and verification interface | Doreen – Verification and Frontend UI Specialist | Mncedisi (Artwell) reviews search integration |
| FR-AUD, NFR-TEST and documentation QA | Cleopatra – Audit Trail and QA Lead | Every author supplies tests and evidence |
| IAM and security controls | Shared, coordinated by project lead | At least one independent security-focused review |

## 13. Release acceptance criteria

The system shall not be described as release-ready until all of the following are evidenced:

1. The project lead confirms the approved baseline and requirement scope.
2. Every mandatory requirement is linked to implementation and test evidence in the traceability matrix.
3. Unit and integration tests pass on a clean checkout.
4. CI quality checks pass for the release commit.
5. Critical access-control and personal-data disclosure defects are resolved.
6. The shared deployment uses persistent data storage and loads required static assets.
7. User, administrator, API, architecture, testing and deployment documents match the demonstrated system.
8. Each member's genuine issues, commits, pull requests and reviews are identifiable.
9. The team completes and records acceptance testing.
10. The project lead approves and tags the tested release.

## 14. Assumptions and constraints

- The project is an academic demonstration and shall use fictional data.
- The assignment permits Python or Java; the current repository uses Python and Django.
- Git, pull requests, code review, issue tracking and CI/CD evidence are assessed outcomes, not optional administration.
- Antigravity or another coding assistant is not an assignment requirement and shall not replace genuine individual contribution or understanding.
- Multiple certificates per student, exact-only public verification, the detailed role matrix and performance targets are proposed project refinements, not quotations of the assignment. Record scope approval in the table below before treating them as agreed implementation commitments.
- Exact institutional retention periods, employer-consent procedures and production service levels require confirmation by the system owner before real-world use.
- Any optional bonus feature shall be implemented only after the four core requirements and their security controls pass acceptance testing.

## 15. Approval record

| Review role | Name | Decision | Date |
|---|---|---|---|
| Project Lead and DevOps Architect | Charlton | Pending | — |
| Database and Registry Lead | Simba | Pending | — |
| Search and Retrieval Specialist | Mncedisi (Artwell) | Pending | — |
| Verification and Frontend UI Specialist | Doreen | Pending | — |
| Audit Trail and QA Lead | Cleopatra | Pending | — |

## 16. References

- MIM736 Practical Assignment – August 2026: *Design and Implement a DevOps-Enabled Qualification Verification System Using Git and CI/CD Practices*.
- Current MSU QVS repository models, views, URLs, tests, Docker configuration and CI workflow inspected for compatibility with this specification.
- `README.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/API_DOCUMENTATION.md`, `docs/USER_MANUAL.md` and `docs/ADMINISTRATOR_MANUAL.md`.
