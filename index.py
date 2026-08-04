import os
import sys

# Configure Python path for Vercel Serverless environment
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msu_qvs.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
