import os
import sys
from pathlib import Path

# Add backend and root directories to sys.path for Vercel Serverless Function
root_dir = Path(__file__).resolve().parent.parent
backend_dir = root_dir / 'backend'

sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(root_dir))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msu_qvs.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
