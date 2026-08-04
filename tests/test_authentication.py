import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
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
