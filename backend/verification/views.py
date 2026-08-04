from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from qualifications.models import Certificate
from students.models import Student
from .models import VerificationLog
from .utils import generate_verification_pdf_report, generate_certificate_qr_code
from ai_fraud.detector import AIFraudDetector

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home_view(request):
    """Public Landing Page with Verification Form."""
    recent_verifications = VerificationLog.objects.select_related('certificate').all()[:5]
    total_verified = Certificate.objects.filter(status='ACTIVE').count()
    return render(request, 'index.html', {
        'total_verified': total_verified,
        'recent_verifications': recent_verifications
    })

def qr_scanner_view(request):
    """Interactive Web UI Camera QR Scanner."""
    return render(request, 'qr_scanner.html')

def verify_qualification(query_string, search_type=None):
    """
    Core Verification Engine Logic.
    Finds certificate by cert_number, verification_code, student_number, national_id, or name.
    """
    query_string = query_string.strip()
    cert = None
    
    # 1. Direct Certificate Number match
    cert = Certificate.objects.filter(certificate_number__iexact=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.CERTIFICATE_NUMBER
        
    # 2. Verification Code match
    cert = Certificate.objects.filter(verification_code__iexact=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.VERIFICATION_CODE
        
    # 3. Student Number match
    cert = Certificate.objects.filter(student__student_number__iexact=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.STUDENT_NUMBER

    # 4. National ID match
    cert = Certificate.objects.filter(student__national_id__iexact=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.NATIONAL_ID

    # 5. Full Name fuzzy match
    cert = Certificate.objects.filter(student__full_name__icontains=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.NAME

    return None, search_type or VerificationLog.SearchType.CERTIFICATE_NUMBER

def verify_view(request):
    """Web view to process qualification verification search."""
    query = request.GET.get('query', '').strip() or request.GET.get('code', '').strip() or request.GET.get('cert', '').strip()
    
    if not query:
        return render(request, 'verify.html', {'error': 'Please enter a Certificate Number, Student Number, or Verification Code.'})

    cert, determined_search_type = verify_qualification(query)
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # AI Fraud Evaluation
    is_suspicious, anomaly_score, fraud_reason = AIFraudDetector.evaluate_verification_request(
        query=query,
        search_type=determined_search_type,
        certificate=cert,
        ip_address=ip_address,
        user_agent=user_agent
    )

    if cert:
        if cert.status == Certificate.Status.ACTIVE:
            result_status = VerificationLog.ResultStatus.VERIFIED
        elif cert.status == Certificate.Status.REVOKED:
            result_status = VerificationLog.ResultStatus.REVOKED
        else:
            result_status = VerificationLog.ResultStatus.PENDING
    else:
        result_status = VerificationLog.ResultStatus.INVALID

    # Create Verification Log
    user = request.user if request.user.is_authenticated else None
    log = VerificationLog.objects.create(
        search_query=query,
        search_type=determined_search_type,
        result_status=result_status,
        certificate=cert,
        verified_by=user,
        ip_address=ip_address,
        user_agent=user_agent,
        is_suspicious=is_suspicious,
        anomaly_score=anomaly_score,
        fraud_reason=fraud_reason
    )

    # Ensure QR code image exists for valid certificate
    if cert and not cert.qr_code_image:
        generate_certificate_qr_code(cert, request)

    return render(request, 'verify.html', {
        'query': query,
        'certificate': cert,
        'verification_log': log,
        'result_status': result_status,
        'is_suspicious': is_suspicious,
        'anomaly_score': anomaly_score,
        'fraud_reason': fraud_reason
    })

def download_verification_pdf(request, log_id):
    """Generate and return PDF Verification Report."""
    log = get_object_or_404(VerificationLog.objects.select_related('certificate', 'certificate__student', 'certificate__qualification'), id=log_id)
    pdf_buffer = generate_verification_pdf_report(log, log.certificate)
    
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="MSU_Verification_Report_{log.id}.pdf"'
    return response

# REST API Endpoint for Verification
class APIVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        query = request.data.get('query') or request.data.get('code') or request.data.get('certificate_number')
        if not query:
            return Response({'error': 'Parameter "query", "code", or "certificate_number" is required.'}, status=status.HTTP_400_BAD_REQUEST)

        cert, search_type = verify_qualification(query)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        is_suspicious, anomaly_score, fraud_reason = AIFraudDetector.evaluate_verification_request(
            query=query,
            search_type=search_type,
            certificate=cert,
            ip_address=ip_address,
            user_agent=user_agent
        )

        if cert:
            if cert.status == Certificate.Status.ACTIVE:
                result_status = VerificationLog.ResultStatus.VERIFIED
            elif cert.status == Certificate.Status.REVOKED:
                result_status = VerificationLog.ResultStatus.REVOKED
            else:
                result_status = VerificationLog.ResultStatus.PENDING
        else:
            result_status = VerificationLog.ResultStatus.INVALID

        user = request.user if request.user.is_authenticated else None
        log = VerificationLog.objects.create(
            search_query=query,
            search_type=search_type,
            result_status=result_status,
            certificate=cert,
            verified_by=user,
            ip_address=ip_address,
            user_agent=user_agent,
            is_suspicious=is_suspicious,
            anomaly_score=anomaly_score,
            fraud_reason=fraud_reason
        )

        data = {
            'verification_id': log.id,
            'query': query,
            'status': result_status,
            'timestamp': log.timestamp.isoformat(),
            'ai_fraud_check': {
                'is_suspicious': is_suspicious,
                'anomaly_score': anomaly_score,
                'reasons': fraud_reason
            }
        }

        if cert and cert.student:
            student = cert.student
            data['certificate_details'] = {
                'certificate_number': cert.certificate_number,
                'verification_code': cert.verification_code,
                'digital_signature_hash': cert.digital_signature_hash,
                'student_name': student.full_name,
                'student_number': student.student_number,
                'national_id': student.national_id,
                'programme': student.programme,
                'faculty': student.faculty,
                'level': student.level,
                'degree_classification': student.degree_classification,
                'graduation_date': str(student.graduation_date),
            }

        return Response(data, status=status.HTTP_200_OK if result_status == 'VERIFIED' else status.HTTP_404_NOT_FOUND if result_status == 'INVALID' else status.HTTP_200_OK)
