from django.db import models
from django.conf import settings
from qualifications.models import Certificate

class VerificationLog(models.Model):
    class SearchType(models.TextChoices):
        CERTIFICATE_NUMBER = 'CERTIFICATE_NUMBER', 'Certificate Number'
        STUDENT_NUMBER = 'STUDENT_NUMBER', 'Student Number'
        VERIFICATION_CODE = 'VERIFICATION_CODE', 'Verification Code'
        QR_CODE = 'QR_CODE', 'QR Code Scan'
        NATIONAL_ID = 'NATIONAL_ID', 'National ID'
        NAME = 'NAME', 'Student Name'

    class ResultStatus(models.TextChoices):
        VERIFIED = 'VERIFIED', 'Verified / Valid'
        INVALID = 'INVALID', 'Invalid / Not Found'
        REVOKED = 'REVOKED', 'Revoked'
        PENDING = 'PENDING', 'Pending Verification'

    search_query = models.CharField(max_length=150)
    search_type = models.CharField(max_length=30, choices=SearchType.choices, default=SearchType.CERTIFICATE_NUMBER)
    result_status = models.CharField(max_length=20, choices=ResultStatus.choices)
    certificate = models.ForeignKey(Certificate, on_delete=models.SET_NULL, null=True, blank=True, related_name='verifications')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    is_suspicious = models.BooleanField(default=False)
    fraud_reason = models.TextField(blank=True, null=True)
    anomaly_score = models.IntegerField(default=0, help_text="0 to 100 Risk Score")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.search_query} -> {self.result_status} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"
