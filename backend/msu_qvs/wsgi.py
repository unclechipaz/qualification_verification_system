import os
import sys
from pathlib import Path

# Add backend directory to sys.path so all app modules (authentication, students, etc.) are importable on Vercel
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msu_qvs.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
app = application
