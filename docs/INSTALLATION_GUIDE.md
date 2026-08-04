# Midlands State University QVS - Installation & Cloud Deployment Guide

## 1. Local Quick Start (Zero External Dependencies)

### Prerequisites:
- Python 3.13+ installed

### Steps:
```bash
# 1. Clone repository
git clone https://github.com/midlands-state-university/qualification-verification-system.git
cd qualification_verification_system

# 2. Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Apply migrations
python backend/manage.py makemigrations
python backend/manage.py migrate

# 5. Seed database with MSU default test data
python backend/manage.py seed_db

# 6. Run development server
python backend/manage.py runserver 0.0.0.0:8000
```
Open your browser at `http://localhost:8000/`.

---

## 2. Docker & Docker Compose Deployment

```bash
# Build and run containers (PostgreSQL + Django)
docker-compose -f docker/docker-compose.yml up --build
```
The application will automatically wait for PostgreSQL, apply migrations, seed demo data, and start on `http://localhost:8000/`.

---

## 3. Cloud Deployment Readiness

### Deploy to Render / Railway:
1. Connect your GitHub repository to Render/Railway.
2. Environment Variables:
   - `DB_ENGINE`: `django.db.backends.postgresql`
   - `DATABASE_URL`: Provided by Render/Railway PostgreSQL service
   - `SECRET_KEY`: Set your secret key
   - `DEBUG`: `False`
3. Build Command: `pip install -r requirements.txt && python backend/manage.py migrate && python backend/manage.py seed_db`
4. Start Command: `gunicorn --chdir backend msu_qvs.wsgi:application`

### Deploy to AWS / DigitalOcean / Azure:
- Use the included `docker/Dockerfile` to deploy as a container service (AWS ECS, DigitalOcean App Platform, Azure Container Apps).
