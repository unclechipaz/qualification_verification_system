import datetime

import pytest
from django.core.cache import cache

from qualifications.models import Certificate, Qualification
from students.models import Student


@pytest.fixture(autouse=True)
def isolated_test_storage(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / 'media'
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def issued_certificate(db):
    student = Student.objects.create(
        student_number='R299999T', national_id='63-7654321-A-07',
        full_name='Synthetic Quality Graduate', programme='BSc Computing',
        faculty='Science', level='Undergraduate',
        graduation_date=datetime.date(2026, 6, 1), qualification='BSc Computing',
        degree_classification='First', status=Student.Status.GRADUATED,
    )
    qualification = Qualification.objects.create(
        title='BSc Computing', code='QUALITY', faculty='Science', department='Computing',
    )
    certificate = Certificate.objects.create(
        student=student, qualification=qualification,
        certificate_number='MSU-2026-QUALITY-001', issue_date=datetime.date(2026, 6, 1),
    )
    certificate.refresh_from_db()
    return certificate
