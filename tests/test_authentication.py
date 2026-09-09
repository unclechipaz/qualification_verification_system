import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestAuthentication:
    def test_user_creation_with_role(self):
        user = User.objects.create_user(
            username='testregistrar',
            email='registrar@msu.ac.zw',
            password='TestPassword123!',
            role=User.Role.REGISTRAR
        )
        assert user.role == 'REGISTRAR'
        assert user.is_admin_or_registrar() is True

    def test_api_login_success(self):
        client = APIClient()
        User.objects.create_user(username='apiuser', password='ApiPassword123!')
        
        response = client.post('/api/login/', {'username': 'apiuser', 'password': 'ApiPassword123!'})
        assert response.status_code == 200
        assert 'token' in response.data

    def test_api_login_failure(self):
        client = APIClient()
        response = client.post('/api/login/', {'username': 'wrong', 'password': 'bad'})
        assert response.status_code == 401

    def test_web_registration_rejects_privileged_role(self):
        client = Client()
        response = client.post('/auth/register/', {
            'username': 'attacker',
            'email': 'attacker@example.com',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
            'role': User.Role.ADMINISTRATOR,
        })

        assert response.status_code == 200
        assert not User.objects.filter(username='attacker').exists()

    def test_web_registration_enforces_password_validation(self):
        client = Client()
        response = client.post('/auth/register/', {
            'username': 'weakwebuser',
            'email': 'weakwebuser@example.com',
            'password': 'password',
            'confirm_password': 'password',
            'role': User.Role.PUBLIC_VERIFIER,
        })

        assert response.status_code == 200
        assert not User.objects.filter(username='weakwebuser').exists()

    def test_api_registration_rejects_privileged_role(self):
        client = APIClient()
        response = client.post('/api/register/', {
            'username': 'apiattacker',
            'email': 'apiattacker@example.com',
            'password': 'StrongPassword123!',
            'role': User.Role.REGISTRAR,
        })

        assert response.status_code == 400
        assert not User.objects.filter(username='apiattacker').exists()

    def test_api_registration_enforces_password_validation(self):
        client = APIClient()
        response = client.post('/api/register/', {
            'username': 'weakapiuser',
            'email': 'weakapiuser@example.com',
            'password': 'password',
            'role': User.Role.PUBLIC_VERIFIER,
        })

        assert response.status_code == 400
        assert 'password' in response.data
        assert not User.objects.filter(username='weakapiuser').exists()

    def test_login_rejects_external_next_redirect(self):
        client = Client()
        User.objects.create_user(username='safeuser', password='SafePassword123!')

        response = client.post(
            '/auth/login/?next=https://attacker.example/phishing',
            {'username': 'safeuser', 'password': 'SafePassword123!'},
        )

        assert response.status_code == 302
        assert response.url == '/reports/dashboard/'

    def test_login_allows_local_next_redirect(self):
        client = Client()
        User.objects.create_user(username='localuser', password='SafePassword123!')

        response = client.post(
            '/auth/login/?next=/reports/dashboard/',
            {'username': 'localuser', 'password': 'SafePassword123!'},
        )

        assert response.status_code == 302
        assert response.url == '/reports/dashboard/'
