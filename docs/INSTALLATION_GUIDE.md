# MSU QVS: Installation and Deployment Guide

**Delivery update:** Use the [current delivery runbook](CI_CD_DELIVERY.md) for production Docker deployment. Install `requirements-dev.txt` to run tests. Docker startup now applies committed migrations and does not seed demo accounts automatically. The historical baseline and environment notes below predate this change.

**Source baseline:** `0faeb043c8c2c602008b1c7e1d45eb29efdcd098`, reviewed on 10 September 2026.

These instructions support local development and demonstration. They do not establish that the current application or hosted deployment is suitable for production.

## Prerequisites

- Git and Python 3.13 for the runtime targeted by the repository's CI and Docker configuration.
- Internet access to obtain dependencies. The templates also load frontend assets from external CDNs.
- Docker with Compose only if using the container option.

The dependency declaration is `Django 5.2 LTS`, not an unrestricted Django 5.x range. Other requirements use minimum versions rather than a complete lock file. Django's [5.1 documentation](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/) identifies that release series as unsupported; a tested dependency upgrade is part of the remaining deployment work.

## Windows PowerShell

Open PowerShell in the directory where you want the project. These commands use the virtual environment's interpreter directly, so activating a PowerShell script is unnecessary.

```powershell
git clone --branch develop https://github.com/unclechipaz/qualification_verification_system.git
cd qualification_verification_system
py -3.13 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:DB_ENGINE = "django.db.backends.sqlite3"
$env:DB_NAME = Join-Path $env:USERPROFILE "msu-qvs-demo.sqlite3"
$env:DJANGO_SECRET_KEY = & .\venv\Scripts\python.exe -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
.\venv\Scripts\python.exe backend/manage.py migrate --noinput
.\venv\Scripts\python.exe backend/manage.py seed_db
.\venv\Scripts\python.exe backend/manage.py runserver 127.0.0.1:8000
```

Use a new database filename if that path already contains data you need to preserve. The demo database is outside the repository so normal source changes do not include it.

Open `http://127.0.0.1:8000/`. Stop the server with **Ctrl+C**. When opening a new terminal, set the same database variables again before running management commands. Keep a consistent private secret key for a continuing environment; regenerating it invalidates existing sessions. You do not need to rerun the seed command to restart the server.

## Linux or macOS

```bash
git clone --branch develop https://github.com/unclechipaz/qualification_verification_system.git
cd qualification_verification_system
python3.13 -m venv venv
venv/bin/python -m pip install -r requirements-dev.txt
export DB_ENGINE=django.db.backends.sqlite3
export DB_NAME="$HOME/msu-qvs-demo.sqlite3"
export DJANGO_SECRET_KEY="$(venv/bin/python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
venv/bin/python backend/manage.py migrate --noinput
venv/bin/python backend/manage.py seed_db
venv/bin/python backend/manage.py runserver 127.0.0.1:8000
```

The same database and secret-key considerations apply as for Windows. Do not run `makemigrations` as a routine installation step: the repository already contains migrations.

## Demonstration data

`seed_db` applies migrations and, on a fresh database, creates four users, three qualification definitions, three students, three certificates, an employer profile and two sample verification logs.

| Role | Username | Demonstration password |
| --- | --- | --- |
| Administrator | `admin` | `AdminPass123!` |
| Registrar | `registrar` | `RegistrarPass123!` |
| Employer | `employer1` | `EmployerPass123!` |
| Graduate | `graduate1` | `GraduatePass123!` |

These passwords are public fixtures. Each seed run resets these accounts' passwords and appends two verification logs. Existing records created through `get_or_create` are not necessarily updated to match the fixture defaults. The command is not an idempotent production provisioning procedure.

The registrar fixture has `is_staff=True`, but the seed command does not assign Django model permissions. Its application role and Django-admin permissions are separate.

Useful sample identifiers:

- Active: `MSU-2024-BSC-CS-0001` or student `R201452X`.
- Revoked: `MSU-2023-BCOM-ACC-0099`.
- Verification codes are generated values; obtain them from the actual certificate record.

Use these accounts and records only in an isolated demonstration database. The repository also tracks a SQLite database; the commands above explicitly select a separate database instead.

## Checks and tests

Run from the repository root, using your virtual environment's Python:

```bash
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python -m pytest --tb=short
```

If you did not activate the environment, replace `python` with `.\venv\Scripts\python.exe` on Windows or `venv/bin/python` on Linux/macOS.

Use `python -m pytest` to match the CI invocation and include the repository root on Python's import path. The suite currently contains 13 tests. Its `--nomigrations` option means migration application needs separate validation. Passing these tests does not establish complete security, UI, performance, accessibility or deployment coverage.

## Docker demonstration

From the repository root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

The development configuration starts PostgreSQL 16 and Django's development server on port 8000. Compose waits for the database health check. The entrypoint applies committed migrations and then starts the server.

Demo seeding is now an explicit command: `docker compose -f docker/docker-compose.yml exec web python backend/manage.py seed_db`. Run it only against disposable data. The development Compose file includes demonstration database credentials and mounts the source directory; the database port is not published. Use the separate production Compose file for persistent deployment.

Stop containers while preserving their database volume with:

```bash
docker compose -f docker/docker-compose.yml down
```

Do not add `--volumes` unless you intend to delete the demonstration database volume.

## Environment variables actually read

| Variable | Behaviour in the current settings |
| --- | --- |
| `DJANGO_SECRET_KEY` | Supplies Django's secret. If absent, the code uses a hard-coded development fallback. `SECRET_KEY` is not the environment-variable name this project reads. |
| `DB_ENGINE` | Selects PostgreSQL only when exactly `django.db.backends.postgresql`; other values follow the SQLite branch. |
| `DB_NAME` | PostgreSQL database name, or the SQLite file path. |
| `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL connection settings. |
| `VERCEL` | Affects SQLite/media paths. The value `1` also selects the environment-controlled debug expression. |
| `DEBUG` | Read only when `VERCEL=1`. Outside that condition, the code sets `DEBUG=True`, even if the environment says `False`. |

`DATABASE_URL` is not parsed. `ALLOWED_HOSTS` is a fixed list containing `*`, and `CORS_ALLOW_ALL_ORIGINS=True` is hard-coded. Merely defining environment variables with those names does not change the settings. Although `python-dotenv` is installed, the settings do not call it to load a `.env` file.

## Deployment status and remaining work

The [CI/CD delivery runbook](CI_CD_DELIVERY.md) is the current guide for the production Docker image, persistent PostgreSQL/media volumes, Gunicorn, WhiteNoise static assets and GHCR image delivery. Runtime dependencies are pinned on Django 5.2 LTS, and startup applies committed migrations without generating migrations or seeding demo accounts.

The team must still provision and verify its persistent HTTPS deployment, retain backup/restore evidence and resolve the application privacy/authorisation and verification gaps identified in the technical report. Use synthetic data until those controls are verified. The existing Vercel entry point remains separate; its SQLite `/tmp` copy does not provide a shared durable registry.

Record the approved commit, published image digest, deployed URL and successful post-deployment checks. A successful Docker build or disposable CI deployment does not establish permanent service availability.

## Troubleshooting

- **Django or another package cannot be imported:** use the interpreter from the virtual environment where dependencies were installed.
- **pytest cannot import the project:** run `python -m pytest` from the repository root.
- **Tables are missing:** confirm `DB_NAME` points to the intended database and run `migrate`.
- **A protected page redirects to a missing login page:** open `/auth/login/` directly. `LOGIN_URL` has not been set to that route.
- **A local QR opens the Vercel site:** displayed QR data uses a fixed public URL; use a local manual identifier until the code is made environment-aware.
