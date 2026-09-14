# CI/CD delivery and deployment runbook

This change replaces the build-only pipeline with quality gates, container deployment tests and continuous delivery to GitHub Container Registry (GHCR). The working branch starts from develop commit `e12f7d92e280e8a8fc7714a67154d69692d906e3`. Charlton/project lead reviews and merges the pull request into `develop`.

## What the pipeline does

| Stage | Automatic checks or output | Failure behaviour |
| --- | --- | --- |
| Quality | Pinned dependencies, `pip check`, Ruff E4/E7/E9/F/I rules, Django checks, migration drift, migration application, pytest on PostgreSQL 16, at least 80% backend statement coverage | Stops container build and delivery |
| Container | Non-root Gunicorn image, production settings, committed migrations, readiness/revision checks, home/CSS/JS requests, persistence after container recreation, no seeded users | Stops delivery |
| Delivery | Publishes the exact tested image to GHCR on successful pushes to `develop` or `main`; records its immutable digest and source commit | No successful release manifest if publication fails |

Pull requests and feature/fix/docs branch pushes run the quality and container checks. Publication is restricted to successful integration/release branch push events. Only the separate publication job receives `packages: write`; PR jobs have read-only repository permissions. No deployment credentials are exposed to PR code. GitHub's built-in `GITHUB_TOKEN` authenticates publication. Repository/package policy must permit that job to publish; do not paste a personal token into the workflow.

Continuous delivery makes a tested release artifact available. The Docker deployment on a GitHub runner is disposable validation, not the permanent public service. This workflow does not alter the existing Vercel deployment. An operator promotes a selected image digest to the persistent environment below.

## Evidence for the assignment

Open **Actions → MSU QVS CI/CD Pipeline → the run for the submitted commit**. Record the run URL and all job conclusions. Download:

- `quality-evidence-<sha>`: JUnit XML, coverage XML/JSON/HTML and Ruff JSON (14 days).
- `deployment-evidence-<sha>`: production-check log, container logs, health/revision/static checks before and after recreation (14 days).
- `release-manifest-<sha>`: `release.env` containing `QVS_IMAGE` with the published digest and `APP_REVISION` (90 days, successful delivery only).

Download the evidence before it expires and retain it with the assignment. Test reports from failed runs remain evidence of failure, not acceptance. The temporary tested-image artifact is retained for one day for transfer between jobs; rerun the full workflow if it expires before publication.

Coverage measures backend Python statements, including settings, operational endpoints, views and models. Generated migrations are excluded from the coverage percentage and Ruff style checks; their committed contents are preserved and executed on PostgreSQL. It does not measure JavaScript, browser usability or load performance. The 80% threshold is the team's documented target. Ruff checks imports and selected Python correctness/style rules; it is not a complete security scanner or full PEP 8 certification.

The production check deliberately retains HSTS subdomain/preload warnings (W005/W021): enrolling all subdomains or requesting browser preload requires the domain owner's decision. Other production invariants are enforced through configuration errors and tests. `check --deploy` fails on errors and its warnings remain in the evidence; none are silently suppressed.

## Run checks locally

Use Python 3.12 or 3.13 and an isolated virtual environment. Install developer dependencies, not just the runtime image dependencies:

```bash
python -m pip install -r requirements-dev.txt
python -m pip check
ruff check backend tests scripts index.py
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python -m pytest --cov=backend --cov-report=term-missing
```

On Windows, prefix Python commands with your virtual environment interpreter, for example `.\venv\Scripts\python.exe`, and use `.\venv\Scripts\ruff.exe` for Ruff. Local tests default to SQLite; GitHub runs the same suite with PostgreSQL. The suite applies committed migrations; `--nomigrations` has been removed. Tests isolate generated media and reset the throttle cache between test cases.

Django and its runtime dependencies are pinned in `requirements.txt`; testing tools are pinned in `requirements-dev.txt`. The tested framework line is Django 5.2 LTS. Review dependency updates through a PR and rerun all gates.

## Persistent Docker deployment

Use a Docker host with Docker Compose v2 supporting `up --wait` and an HTTPS reverse proxy. The default binding is loopback; the database has no published host port. Use synthetic records until the application access-control and verification findings in the technical report have been resolved.

1. After a successful delivery run, download `release.env`. Preserve its digest and `APP_REVISION` as the release record.
2. From the reviewed checkout, copy `docker/production.env.example` to `docker/production.env`. Set `QVS_IMAGE` to the digest from `release.env`, set the actual hostname, and supply fresh secret values. The example deliberately contains no usable secrets. Generate each secret locally with `python -c "import secrets; print(secrets.token_urlsafe(64))"`; do not commit or share the output.
3. If the GHCR package is private, sign in with credentials permitted to read that package. Public visibility is a package-owner decision; repository visibility does not automatically prove package visibility.
4. Place the host behind HTTPS. Set `DJANGO_CSRF_ORIGINS` to its HTTPS origin. Set `DJANGO_TRUST_PROXY_SSL_HEADER=true` only when the proxy removes client-supplied forwarding headers and supplies its own trusted protocol header.
5. Deploy from the repository root:

```bash
docker compose --env-file docker/production.env -p msu-qvs -f docker/compose.production.yml pull
docker compose --env-file docker/production.env -p msu-qvs -f docker/compose.production.yml up -d --wait --wait-timeout 180
```

6. Run the read-only smoke check against the HTTPS site, replacing the example URL and revision with the recorded values:

```bash
python scripts/smoke_test.py --base-url https://qvs.example.org --expected-revision REPLACE_WITH_APP_REVISION
```

7. Record the URL, digest, revision, date and observed results for the submission. Confirm critical user workflows with synthetic data; a healthy landing page alone is insufficient.

PostgreSQL records and generated QR media use separate named volumes. Keep the project name `msu-qvs` consistent between releases so Compose reuses those volumes. Static assets are collected into the image and served by WhiteNoise with DEBUG disabled. Media is not exposed by a generic public file route; current certificate templates use inline QR images. Do not put user media into the static directory.

The web container applies existing migrations once at startup and exits on failure; it never runs `makemigrations` or `seed_db`. This configuration is for one application service. Coordinate migrations separately before scaling to multiple service replicas. Create the first real administrative account explicitly:

```bash
docker compose --env-file docker/production.env -p msu-qvs -f docker/compose.production.yml exec web python backend/manage.py createsuperuser
```

Django staff/superuser access and application roles are separate; set the intended application role through authorised administration. For local development only, `docker/docker-compose.yml` still supports the bind-mounted development server. Run `seed_db` explicitly only against a disposable demonstration database: it resets known-password demo accounts.

For an isolated local HTTP demonstration, set `DJANGO_SSL_REDIRECT=false` while keeping the binding on `127.0.0.1`; this is not an HTTPS production configuration. Secure-cookie settings stay enabled, so use HTTPS for session-based demonstrations. Never expose that HTTP override as the public service.

## Rollback and remaining release work

Before applying a release, retain the previous image digest, back up PostgreSQL and media and review the migration plan. An image rollback does not undo database migrations. If schema compatibility permits rollback, restore the previous `QVS_IMAGE` in the private environment file and rerun `pull`/`up --wait`. Run the same revision and workflow checks. Do not run `down --volumes` on the persistent stack; that cleanup belongs only to disposable CI.

Charlton should configure the quality and container jobs as required branch checks and retain independent PR review. This change does not itself enable branch protection, merge develop into main, resolve application authorisation/lifecycle defects or verify the existing Vercel release. The technical report remains a dated assessment of its original source commit; add the new successful run and deployment evidence after integration, rather than relabelling its historical results.

The inspection's registrar privilege escalation, certificate/PDF ownership gaps, inconsistent suspended/student-revocation decisions, scanner decoding, history integrity and web-throttling gaps remain separate application work. No acceptance is asserted for those requirements here.

## References

- [GitHub: publishing Docker images](https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images)
- [GitHub: container registry authentication and visibility](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Django 5.2 deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Django configuration](https://whitenoise.readthedocs.io/en/stable/django.html)

Prepared with AI assistance for implementation, tests and documentation. Execution results must be attributed to the actual environment and commit that produced them.
