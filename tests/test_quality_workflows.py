import io

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from pypdf import PdfReader
from rest_framework.test import APIClient

from verification.models import VerificationLog
from verification.utils import generate_verification_pdf_report, mask_national_id

User = get_user_model()
pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('field', ['student_number', 'national_id', 'full_name'])
def test_public_identity_search_does_not_disclose_certificate(issued_certificate, field):
    response = APIClient().post('/api/verify/', {'query': getattr(issued_certificate.student, field)}, format='json')
    assert response.status_code == 404
    assert response.data['status'] == 'INVALID'
    assert 'certificate_details' not in response.data
    assert issued_certificate.student.national_id.encode() not in response.content


@pytest.mark.parametrize('field', ['student_number', 'national_id', 'full_name'])
def test_registrar_identity_search_masks_id_and_log(issued_certificate, field):
    client = APIClient()
    registrar = User.objects.create_user(username='registrar-quality', role='REGISTRAR')
    client.force_authenticate(registrar)
    response = client.post('/api/verify/', {'query': getattr(issued_certificate.student, field)}, format='json')
    assert response.status_code == 200
    assert response.data['status'] == 'VERIFIED'
    assert issued_certificate.student.national_id.encode() not in response.content
    assert VerificationLog.objects.get().verified_by == registrar
    if field == 'national_id':
        assert VerificationLog.objects.get().search_query == mask_national_id(issued_certificate.student.national_id)


@pytest.mark.parametrize('field', ['certificate_number', 'verification_code'])
def test_public_certificate_verification_omits_national_id(issued_certificate, field):
    response = APIClient().post('/api/verify/', {'query': getattr(issued_certificate, field)}, format='json')
    assert response.status_code == 200
    assert response.data['status'] == 'VERIFIED'
    assert issued_certificate.student.national_id.encode() not in response.content


def test_pdf_contains_result_and_masks_national_id(issued_certificate):
    log = VerificationLog.objects.create(
        certificate=issued_certificate, search_query=issued_certificate.certificate_number,
        search_type='CERTIFICATE_NUMBER', result_status='VERIFIED',
    )
    pdf = generate_verification_pdf_report(log, issued_certificate)
    text = '\n'.join(page.extract_text() for page in PdfReader(pdf).pages)
    assert issued_certificate.student.full_name in text
    assert issued_certificate.certificate_number in text
    assert 'VERIFIED' in text
    assert mask_national_id(issued_certificate.student.national_id) in text
    assert issued_certificate.student.national_id not in text


def test_invalid_pdf_reports_unmatched_query():
    log = VerificationLog.objects.create(search_query='NO-SUCH-RECORD', search_type='UNKNOWN', result_status='INVALID')
    pdf = generate_verification_pdf_report(log)
    text = '\n'.join(page.extract_text() for page in PdfReader(io.BytesIO(pdf.read())).pages)
    assert 'INVALID' in text and 'NO-SUCH-RECORD' in text


def test_employer_export_and_portal_isolate_history(client, issued_certificate):
    employer = User.objects.create_user(username='employer-quality', role='EMPLOYER')
    other = User.objects.create_user(username='other-employer', role='EMPLOYER')
    for user, query in [(employer, 'MY-CHECK'), (other, 'OTHER-CHECK')]:
        VerificationLog.objects.create(
            verified_by=user, certificate=issued_certificate, search_query=query,
            search_type='CERTIFICATE_NUMBER', result_status='VERIFIED',
        )
    client.force_login(employer)
    response = client.get(reverse('export_csv'))
    assert response.status_code == 200
    assert b'MY-CHECK' in response.content and b'OTHER-CHECK' not in response.content
    portal = client.get(reverse('employer_portal'))
    assert portal.status_code == 200
    assert portal.context['total_performed'] == 1
    assert list(portal.context['history'].values_list('verified_by_id', flat=True)) == [employer.id]


def test_registrar_dashboard_and_reports_match_records(client, issued_certificate):
    registrar = User.objects.create_user(username='registry-reports', role='REGISTRAR')
    VerificationLog.objects.create(certificate=issued_certificate, search_query='REPORT-CHECK', result_status='VERIFIED')
    client.force_login(registrar)
    dashboard = client.get(reverse('dashboard'))
    assert dashboard.status_code == 200
    assert dashboard.context['total_certificates'] == 1
    assert dashboard.context['total_verifications'] == 1
    reports = client.get(reverse('reports'))
    assert reports.status_code == 200 and reports.context['daily_count'] == 1
    api = APIClient()
    api.force_authenticate(registrar)
    assert api.get('/api/reports/').data['total_verifications'] == 1


def test_public_account_cannot_use_registry_or_admin_reports(client, issued_certificate):
    public = User.objects.create_user(username='public-quality', role='PUBLIC_VERIFIER')
    api = APIClient()
    api.force_authenticate(public)
    for path in ['/api/students/', '/api/qualifications/', '/api/certificates/', '/api/reports/']:
        assert api.get(path).status_code == 403
    client.force_login(public)
    assert client.get(reverse('student_create')).status_code == 302
    assert client.get(reverse('reports')).status_code == 302
    assert client.get(reverse('export_csv')).status_code == 302


def test_registrar_student_search_masks_national_id(client, issued_certificate):
    registrar = User.objects.create_user(username='registry-search', role='REGISTRAR')
    client.force_login(registrar)
    response = client.get(reverse('student_list'), {'q': issued_certificate.student.full_name})
    assert response.status_code == 200
    assert issued_certificate.student.full_name.encode() in response.content
    assert issued_certificate.student.national_id.encode() not in response.content
