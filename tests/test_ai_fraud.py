import pytest
import datetime
from students.models import Student
from qualifications.models import Qualification, Certificate
from ai_fraud.detector import AIFraudDetector

@pytest.mark.django_db
class TestAIFraudDetection:
    def test_revoked_certificate_fraud_detection(self):
        student = Student.objects.create(
            student_number='R111111A',
            national_id='63-1111111-A-11',
            full_name='Fraud Test Graduate',
            programme='LLB Law',
            faculty='Law',
            graduation_date=datetime.date(2023, 11, 20),
            qualification='Bachelor of Laws',
            degree_classification='Pass',
            status='Revoked'
        )
        qual = Qualification.objects.create(title='LLB Law', code='LAW-TEST', faculty='Law', department='Law')
        cert = Certificate.objects.create(
            student=student,
            qualification=qual,
            certificate_number='MSU-2023-REVOKED-001',
            issue_date=datetime.date(2023, 11, 20),
            status=Certificate.Status.REVOKED,
            revocation_reason='Cheating'
        )

        is_suspicious, score, reason = AIFraudDetector.evaluate_verification_request(
            query='MSU-2023-REVOKED-001',
            search_type='CERTIFICATE_NUMBER',
            certificate=cert,
            ip_address='127.0.0.1'
        )

        assert is_suspicious is True
        assert score >= 60
        assert 'REVOKED' in reason
