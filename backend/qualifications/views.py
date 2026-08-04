from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, filters
from authentication.permissions import IsAdminOrRegistrar
from .models import Qualification, Certificate
from .serializers import QualificationSerializer, CertificateSerializer
from students.models import Student
from verification.utils import generate_certificate_qr_code

@login_required
def qualification_list_view(request):
    qualifications = Qualification.objects.all()
    certificates = Certificate.objects.select_related('student', 'qualification').all()
    return render(request, 'qualifications/qualification_list.html', {
        'qualifications': qualifications,
        'certificates': certificates
    })

@login_required
def certificate_detail_view(request, cert_number):
    certificate = get_object_or_404(Certificate.objects.select_related('student', 'qualification'), certificate_number=cert_number)
    
    # Ensure QR code exists
    if not certificate.qr_code_image:
        generate_certificate_qr_code(certificate, request)
        
    return render(request, 'qualifications/certificate_detail.html', {
        'certificate': certificate
    })

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [IsAdminOrRegistrar]

class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.select_related('student', 'qualification').all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAdminOrRegistrar]
    filter_backends = [filters.SearchFilter]
    search_fields = ['certificate_number', 'verification_code', 'student__student_number', 'student__full_name']
