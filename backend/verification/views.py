from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from qualifications.models import Certificate
from students.models import Student
from .models import VerificationLog
from .utils import generate_verification_pdf_report, generate_certificate_qr_code, mask_national_id, is_national_id_format
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

MAX_VERIFICATION_QUERY_LENGTH = 150

def validate_verification_query(raw_query):
    """
    Validates the query for qualification verification.

    Rules:
    - Must not be None.
    - Must be a string (rejects booleans, integers, floats, lists, dicts, etc.).
    - Must not be empty or spaces-only.
    - Must not exceed MAX_VERIFICATION_QUERY_LENGTH (150 chars).

    Returns:
        tuple: (is_valid: bool, cleaned_query_or_error: str)
    """
    if raw_query is None:
        return False, 'Parameter "query", "code", or "certificate_number" is required.'

    # Must be a string and not a boolean (bool is a subclass of int in Python)
    if isinstance(raw_query, bool) or not isinstance(raw_query, str):
        return False, 'Query parameter must be a string.'

    cleaned = raw_query.strip()
    if not cleaned:
        return False, 'Query parameter cannot be empty or spaces only.'

    if len(cleaned) > MAX_VERIFICATION_QUERY_LENGTH:
        return False, f'Query exceeds maximum length of {MAX_VERIFICATION_QUERY_LENGTH} characters.'

    return True, cleaned

def verify_qualification(query_string, search_type=None, is_internal=False):
    """
    Core Verification Engine Logic.

    Public/Anonymous verification (is_internal=False):
      Accepts only exact certificate_number or verification_code (FR-SRCH-08).
      Queries by student_number, national_id, or name are rejected without disclosure (TC-SRCH-011).

    Authorised Internal search (is_internal=True):
      Finds certificate by cert_number, verification_code, student_number, national_id, or name (FR-SRCH-01).
    """
    if isinstance(query_string, bool) or not isinstance(query_string, str):
        return None, search_type or VerificationLog.SearchType.CERTIFICATE_NUMBER

    query_string = query_string.strip()
    if not query_string or len(query_string) > MAX_VERIFICATION_QUERY_LENGTH:
        return None, search_type or VerificationLog.SearchType.CERTIFICATE_NUMBER

    cert = None
    
    # 1. Direct Certificate Number match (allowed for all callers)
    cert = Certificate.objects.filter(certificate_number__iexact=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.CERTIFICATE_NUMBER
        
    # 2. Verification Code match (allowed for all callers)
    cert = Certificate.objects.filter(verification_code__iexact=query_string).select_related('student', 'qualification').first()
    if cert:
        return cert, VerificationLog.SearchType.VERIFICATION_CODE

    # Identity queries are permitted ONLY for authorised internal roles (FR-SRCH-08, FR-SRCH-01)
    if is_internal:
        # 3. Student Number match
        cert = Certificate.objects.filter(student__student_number__iexact=query_string).select_related('student', 'qualification').first()
        if cert:
            return cert, VerificationLog.SearchType.STUDENT_NUMBER

        # 4. National ID match
        cert = Certificate.objects.filter(student__national_id__iexact=query_string).select_related('student', 'qualification').first()
        if cert:
            return cert, VerificationLog.SearchType.NATIONAL_ID

        # 5. Full Name fuzzy match (only non-empty query reaches here)
        cert = Certificate.objects.filter(student__full_name__icontains=query_string).select_related('student', 'qualification').first()
        if cert:
            return cert, VerificationLog.SearchType.NAME

    return None, search_type or VerificationLog.SearchType.CERTIFICATE_NUMBER

def verify_view(request):
    """Web view to process qualification verification search."""
    raw_query = None
    for key in ('query', 'code', 'cert'):
        val = request.GET.get(key)
        if val is not None:
            raw_query = val
            break

    if raw_query is None:
        return render(request, 'verify.html', {'error': 'Please enter a Certificate Number or Verification Code.'})

    is_valid, result = validate_verification_query(raw_query)
    if not is_valid:
        if 'empty or spaces only' in result or 'required' in result:
            error_msg = 'Please enter a Certificate Number or Verification Code.'
        elif 'maximum length' in result:
            error_msg = f'Verification query cannot exceed {MAX_VERIFICATION_QUERY_LENGTH} characters.'
        else:
            error_msg = 'Invalid verification query. Please enter a valid search string.'
        return render(request, 'verify.html', {'error': error_msg})

    query = result
    is_internal = bool(request.user.is_authenticated and request.user.is_admin_or_registrar())
    cert, determined_search_type = verify_qualification(query, is_internal=is_internal)
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Mask query for fraud evaluation and logging if it is or contains a National ID (FR-SRCH-14)
    is_national_id = (determined_search_type == VerificationLog.SearchType.NATIONAL_ID or is_national_id_format(query))
    safe_query = mask_national_id(query) if is_national_id else query

    # AI Fraud Evaluation
    is_suspicious, anomaly_score, fraud_reason = AIFraudDetector.evaluate_verification_request(
        query=safe_query,
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

    # Create Verification Log with masked query if National ID (FR-SRCH-14)
    user = request.user if request.user.is_authenticated else None
    log = VerificationLog.objects.create(
        search_query=safe_query,
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
        'query': safe_query if is_national_id else query,
        'certificate': cert,
        'verification_log': log,
        'result_status': result_status,
        'is_suspicious': is_suspicious,
        'anomaly_score': anomaly_score,
        'fraud_reason': fraud_reason,
        'is_internal': is_internal
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
        if not isinstance(request.data, dict):
            return Response(
                {'error': 'Invalid request body. Expected a JSON object.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        raw_query = None
        has_key = False
        for key in ('query', 'code', 'certificate_number'):
            if key in request.data:
                has_key = True
                val = request.data[key]
                if val is not None:
                    raw_query = val
                    break

        if not has_key or raw_query is None:
            return Response(
                {'error': 'Parameter "query", "code", or "certificate_number" is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, result = validate_verification_query(raw_query)
        if not is_valid:
            return Response({'error': result}, status=status.HTTP_400_BAD_REQUEST)

        query = result
        is_internal = bool(request.user.is_authenticated and request.user.is_admin_or_registrar())
        cert, search_type = verify_qualification(query, is_internal=is_internal)
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Mask query for fraud evaluation and logging if it is or contains a National ID (FR-SRCH-14)
        is_national_id = (search_type == VerificationLog.SearchType.NATIONAL_ID or is_national_id_format(query))
        safe_query = mask_national_id(query) if is_national_id else query

        is_suspicious, anomaly_score, fraud_reason = AIFraudDetector.evaluate_verification_request(
            query=safe_query,
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
            search_query=safe_query,
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
            'query': safe_query if is_national_id else query,
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
            details = {
                'certificate_number': cert.certificate_number,
                'verification_code': cert.verification_code,
                'digital_signature_hash': cert.digital_signature_hash,
                'student_name': student.full_name,
                'student_number': student.student_number,
                'programme': student.programme,
                'faculty': student.faculty,
                'level': student.level,
                'degree_classification': student.degree_classification,
                'graduation_date': str(student.graduation_date),
            }
            # National ID is never exposed to anonymous users; internal users receive masked value (FR-SRCH-07)
            if is_internal:
                details['national_id'] = mask_national_id(student.national_id)
            data['certificate_details'] = details

        return Response(data, status=status.HTTP_200_OK if result_status == 'VERIFIED' else status.HTTP_404_NOT_FOUND if result_status == 'INVALID' else status.HTTP_200_OK)
