import datetime
import pytest
from django.contrib.auth import get_user_model
from students.models import Student
from qualifications.models import Qualification, Certificate
from verification.models import VerificationLog
from verification.views import verify_qualification

User = get_user_model()

@pytest.mark.django_db
class TestVerificationEngine:
    @pytest.fixture
    def sample_data(self):
        student = Student.objects.create(
            student_number='R209999Z',
            national_id='63-0000000-A-00',
            full_name='Verification Test Student',
            programme='BSc Computer Science',
            faculty='Science and Technology',
            level='Undergraduate',
            graduation_date=datetime.date(2024, 11, 20),
            qualification='Bachelor of Science Honors Degree in Computer Science',
            degree_classification='First Class (1.1)',
            status='Graduated'
        )
        qual = Qualification.objects.create(
            title='Bachelor of Science Honors Degree in Computer Science',
            code='BSC-CS-TEST',
            faculty='Science and Technology',
            department='Computer Science'
        )
        cert = Certificate.objects.create(
            student=student,
            qualification=qual,
            certificate_number='MSU-2024-TEST-0001',
            issue_date=datetime.date(2024, 11, 20),
            status=Certificate.Status.ACTIVE
        )
        return student, cert

    def test_verification_by_cert_number(self, sample_data):
        student, cert = sample_data
        found_cert, search_type = verify_qualification('MSU-2024-TEST-0001')
        assert found_cert is not None
        assert found_cert.student.full_name == 'Verification Test Student'

    def test_verification_by_student_number(self, sample_data):
        student, cert = sample_data
        found_cert, search_type = verify_qualification('R209999Z')
        assert found_cert is not None
        assert found_cert.certificate_number == 'MSU-2024-TEST-0001'

    def test_invalid_verification_query(self):
        found_cert, search_type = verify_qualification('NONEXISTENT-CODE')
        assert found_cert is None

    # --- Issue #9 Regression Tests ---

    def test_spaces_only_query_does_not_return_certificate(self, sample_data):
        """Regression test: spaces-only query must not match any certificate."""
        found_cert, search_type = verify_qualification('   ')
        assert found_cert is None

    def test_api_spaces_only_query_rejected(self, sample_data):
        """Regression test: spaces-only query to API must return HTTP 400 and not VERIFIED."""
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/verify/', {'query': '   '}, format='json')
        assert response.status_code == 400
        assert 'error' in response.data

    def test_non_string_inputs_to_helper_handled_gracefully(self, sample_data):
        """Regression test: numbers, booleans, lists, and dicts to helper must not raise unhandled errors."""
        for invalid_input in [12345, True, False, ['MSU-2024-TEST-0001'], {'code': 'MSU-2024-TEST-0001'}, None]:
            found_cert, search_type = verify_qualification(invalid_input)
            assert found_cert is None

    def test_api_non_string_inputs_rejected(self, sample_data):
        """Regression test: non-string query inputs to API must return HTTP 400 instead of 500."""
        from rest_framework.test import APIClient
        client = APIClient()
        for invalid_query in [12345, True, False, ['MSU-2024-TEST-0001'], {'nested': 'val'}]:
            response = client.post('/api/verify/', {'query': invalid_query}, format='json')
            assert response.status_code == 400
            assert 'error' in response.data

    def test_api_malformed_payload_rejected(self, sample_data):
        """Regression test: non-object request body to API must return HTTP 400 instead of 500."""
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post('/api/verify/', [1, 2, 3], format='json')
        assert response.status_code == 400
        assert 'error' in response.data

    def test_overlength_query_rejected(self, sample_data):
        """Regression test: query exceeding 150 chars must be rejected."""
        from rest_framework.test import APIClient
        client = APIClient()
        overlength = 'A' * 151
        found_cert, search_type = verify_qualification(overlength)
        assert found_cert is None

        response = client.post('/api/verify/', {'query': overlength}, format='json')
        assert response.status_code == 400
        assert 'error' in response.data

    def test_web_view_spaces_and_invalid_inputs(self, sample_data):
        """Regression test: web view rejects spaces-only and overlength queries without returning VERIFIED."""
        from django.test import Client
        client = Client()

        # Spaces-only query
        resp = client.get('/verify/', {'query': '   '})
        assert resp.status_code == 200
        assert 'error' in resp.context
        assert resp.context.get('result_status') != 'VERIFIED'
        assert resp.context.get('certificate') is None

        # Overlength query
        resp = client.get('/verify/', {'query': 'A' * 151})
        assert resp.status_code == 200
        assert 'error' in resp.context
        assert resp.context.get('result_status') != 'VERIFIED'
        assert resp.context.get('certificate') is None

    def test_preserves_valid_searches_and_aliases(self, sample_data):
        """Valid queries, surrounding spaces, and supported aliases must be preserved."""
        from rest_framework.test import APIClient
        from django.test import Client
        api_client = APIClient()
        web_client = Client()

        # Surrounding spaces preserved and stripped
        resp = api_client.post('/api/verify/', {'query': '  MSU-2024-TEST-0001  '}, format='json')
        assert resp.status_code == 200
        assert resp.data['status'] == 'VERIFIED'

        # Code alias
        resp = api_client.post('/api/verify/', {'code': 'MSU-2024-TEST-0001'}, format='json')
        assert resp.status_code == 200
        assert resp.data['status'] == 'VERIFIED'

        # Certificate number alias
        resp = api_client.post('/api/verify/', {'certificate_number': 'MSU-2024-TEST-0001'}, format='json')
        assert resp.status_code == 200
        assert resp.data['status'] == 'VERIFIED'

        # Web view surrounding spaces
        resp = web_client.get('/verify/', {'query': '  MSU-2024-TEST-0001  '})
        assert resp.status_code == 200
        assert resp.context.get('result_status') == 'VERIFIED'
        assert resp.context.get('certificate') is not None

        # Web view code alias
        resp = web_client.get('/verify/', {'code': 'MSU-2024-TEST-0001'})
        assert resp.status_code == 200
        assert resp.context.get('result_status') == 'VERIFIED'

    def test_validate_verification_query_unit(self):
        """Direct unit tests for validate_verification_query helper."""
        from verification.views import validate_verification_query

        # Missing / None
        valid, msg = validate_verification_query(None)
        assert not valid
        assert 'required' in msg

        # Empty / Spaces
        for empty_val in ['', '   ', '\t\n']:
            valid, msg = validate_verification_query(empty_val)
            assert not valid
            assert 'empty or spaces' in msg

        # Unsupported types
        for bad_val in [123, 45.67, True, False, ['a'], {'k': 'v'}]:
            valid, msg = validate_verification_query(bad_val)
            assert not valid
            assert 'string' in msg

        # Boundary length: 150 chars (allowed) vs 151 chars (rejected)
        valid_150 = 'A' * 150
        valid, result = validate_verification_query(valid_150)
        assert valid
        assert result == valid_150

        invalid_151 = 'A' * 151
        valid, msg = validate_verification_query(invalid_151)
        assert not valid
        assert 'maximum length' in msg

        # Valid with surrounding spaces
        valid, result = validate_verification_query('  MSU-2024-TEST-0001  ')
        assert valid
        assert result == 'MSU-2024-TEST-0001'

    def test_api_empty_and_missing_payload(self):
        """API must return HTTP 400 for empty or completely missing query parameters."""
        from rest_framework.test import APIClient
        client = APIClient()

        # Completely empty dict
        resp = client.post('/api/verify/', {}, format='json')
        assert resp.status_code == 400
        assert 'error' in resp.data

        # Explicit empty string
        resp = client.post('/api/verify/', {'query': ''}, format='json')
        assert resp.status_code == 400
        assert 'error' in resp.data


