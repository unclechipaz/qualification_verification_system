from rest_framework import serializers
from .models import Qualification, Certificate
from students.serializers import StudentSerializer

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class CertificateSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    qualification_details = QualificationSerializer(source='qualification', read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id', 'student', 'student_details', 'qualification', 'qualification_details',
            'certificate_number', 'verification_code', 'issue_date', 'qr_code_image',
            'status', 'revocation_reason', 'digital_signature_hash', 'created_at'
        ]
        read_only_fields = ['id', 'certificate_number', 'verification_code', 'digital_signature_hash', 'created_at']
