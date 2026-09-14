"""Settings for the persistent Docker deployment; missing secrets fail closed."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from . import settings as base
from .settings import *  # noqa: F403 - inherit the documented development settings


def required(name):
    value = os.environ.get(name, '').strip()
    if not value:
        raise ImproperlyConfigured(f'{name} must be set for production')
    return value


DEBUG = False
SECRET_KEY = required('DJANGO_SECRET_KEY')
if len(SECRET_KEY) < 50 or len(set(SECRET_KEY)) < 5 or SECRET_KEY.startswith('django-insecure-'):
    raise ImproperlyConfigured('DJANGO_SECRET_KEY must be a strong production secret')

ALLOWED_HOSTS = [host.strip() for host in required('DJANGO_ALLOWED_HOSTS').split(',') if host.strip()]
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('DJANGO_ALLOWED_HOSTS must contain explicit hosts')
# Container health checks use loopback and expose no record or environment details.
ALLOWED_HOSTS = list(dict.fromkeys([*ALLOWED_HOSTS, '127.0.0.1', 'localhost']))

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': required('DB_NAME'),
    'USER': required('DB_USER'),
    'PASSWORD': required('DB_PASSWORD'),
    'HOST': required('DB_HOST'),
    'PORT': os.environ.get('DB_PORT', '5432'),
    'CONN_MAX_AGE': 60,
    'CONN_HEALTH_CHECKS': True,
}}

MIDDLEWARE = [base.MIDDLEWARE[0], 'whitenoise.middleware.WhiteNoiseMiddleware', *base.MIDDLEWARE[1:]]
MEDIA_ROOT = Path(os.environ.get('DJANGO_MEDIA_ROOT', str(base.BASE_DIR / 'media')))
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [value.strip() for value in os.environ.get('DJANGO_CORS_ORIGINS', '').split(',') if value.strip()]
CSRF_TRUSTED_ORIGINS = [value.strip() for value in os.environ.get('DJANGO_CSRF_ORIGINS', '').split(',') if value.strip()]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SSL_REDIRECT', 'true').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_HSTS_SECONDS', '31536000' if SECURE_SSL_REDIRECT else '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_HSTS_SUBDOMAINS', 'false').lower() == 'true'
SECURE_HSTS_PRELOAD = False
SECURE_REDIRECT_EXEMPT = [r'^health/live/$', r'^health/ready/$']
if os.environ.get('DJANGO_TRUST_PROXY_SSL_HEADER', 'false').lower() == 'true':
    # Enable only behind a proxy which strips client-supplied forwarding headers.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
