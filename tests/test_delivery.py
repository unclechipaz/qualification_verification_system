import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.db import DatabaseError

PRODUCTION = Path(__file__).resolve().parents[1] / 'backend/msu_qvs/production.py'


@pytest.fixture
def production_environment(monkeypatch):
    values = {
        'DJANGO_SECRET_KEY': 'synthetic-ci-only-secret-1234567890-ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'DJANGO_ALLOWED_HOSTS': 'qvs.example.org',
        'DB_NAME': 'quality_test', 'DB_USER': 'quality_test',
        'DB_PASSWORD': 'synthetic-ci-password', 'DB_HOST': 'db',
    }
    for key, value in values.items():
        monkeypatch.setenv(key, value)
    return values


def load_production():
    spec = importlib.util.spec_from_file_location('backend.msu_qvs._production_test', PRODUCTION)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('missing', ['DJANGO_SECRET_KEY', 'DJANGO_ALLOWED_HOSTS', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST'])
def test_production_rejects_missing_configuration(production_environment, monkeypatch, missing):
    monkeypatch.delenv(missing)
    with pytest.raises(ImproperlyConfigured, match=missing):
        load_production()


@pytest.mark.parametrize('secret', ['short', 'a' * 60, 'django-insecure-' + 'abc123XYZ' * 8])
def test_production_rejects_weak_secrets(production_environment, monkeypatch, secret):
    monkeypatch.setenv('DJANGO_SECRET_KEY', secret)
    with pytest.raises(ImproperlyConfigured, match='strong production secret'):
        load_production()


@pytest.mark.parametrize('hosts', ['*', 'qvs.example.org,*', ', ,'])
def test_production_rejects_unrestricted_hosts(production_environment, monkeypatch, hosts):
    monkeypatch.setenv('DJANGO_ALLOWED_HOSTS', hosts)
    with pytest.raises(ImproperlyConfigured, match='explicit hosts'):
        load_production()


def test_production_security_defaults(production_environment, monkeypatch):
    monkeypatch.setenv('DEBUG', 'true')
    settings = load_production()
    assert settings.DEBUG is False
    assert settings.SESSION_COOKIE_SECURE and settings.CSRF_COOKIE_SECURE
    assert settings.SECURE_SSL_REDIRECT and settings.SECURE_HSTS_SECONDS > 0
    assert not settings.CORS_ALLOW_ALL_ORIGINS
    assert settings.CORS_ALLOWED_ORIGINS == []
    assert not getattr(settings, 'SECURE_PROXY_SSL_HEADER', None)
    assert settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql'
    assert settings.ALLOWED_HOSTS == ['qvs.example.org', '127.0.0.1', 'localhost']


def test_proxy_trust_requires_explicit_setting(production_environment, monkeypatch):
    monkeypatch.setenv('DJANGO_TRUST_PROXY_SSL_HEADER', 'true')
    assert load_production().SECURE_PROXY_SSL_HEADER == ('HTTP_X_FORWARDED_PROTO', 'https')


def test_liveness_does_not_require_database(client, monkeypatch):
    monkeypatch.setenv('APP_REVISION', 'test-revision')
    response = client.get('/health/live/')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok', 'revision': 'test-revision'}
    assert 'no-store' in response['Cache-Control']


@pytest.mark.django_db
def test_readiness_checks_database(client):
    assert client.get('/health/ready/').status_code == 200
    with patch('msu_qvs.health.connection.cursor', side_effect=DatabaseError('private connection details')):
        response = client.get('/health/ready/')
    assert response.status_code == 503
    assert response.json() == {'status': 'unavailable'}
    assert b'private connection details' not in response.content


@pytest.mark.django_db
def test_health_endpoint_rejects_writes(client):
    assert client.post('/health/live/').status_code == 405
    assert client.post('/health/ready/').status_code == 405
