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
