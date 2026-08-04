import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msu_qvs.settings')

application = get_wsgi_application()

# Expose app for Vercel Serverless Function entrypoint
app = application
