import uuid
import hashlib
import io
import base64
import qrcode
from django.db import models
from students.models import Student

class Qualification(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Bachelor of Science Honors Degree in Computer Science")
    code = models.CharField(max_length=50, unique=True, help_text="e.g. BSC-CS")
    faculty = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    duration_years = models.IntegerField(default=4)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.code})"

class Certificate(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active / Valid'
        REVOKED = 'REVOKED', 'Revoked'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='certificate')
    qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT, related_name='certificates')
    certificate_number = models.CharField(max_length=50, unique=True, db_index=True)
    verification_code = models.CharField(max_length=64, unique=True, db_index=True, default=uuid.uuid4)
    issue_date = models.DateField()
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    revocation_reason = models.TextField(blank=True, null=True)
    digital_signature_hash = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            year = self.issue_date.year if self.issue_date else 2024
            code = self.qualification.code if self.qualification else 'GEN'
            last_id = Certificate.objects.count() + 1
            self.certificate_number = f"MSU-{year}-{code}-{last_id:04d}"
            
        if not self.digital_signature_hash and self.student:
            raw_data = f"{self.certificate_number}:{self.student.student_number}:{self.student.national_id}:{self.issue_date}"
            self.digital_signature_hash = hashlib.sha256(raw_data.encode('utf-8')).hexdigest()
            
        super().save(*args, **kwargs)

    @property
    def qr_code_base64(self):
        """Generates self-contained Base64 Data URI QR Code (100% serverless & Vercel compatible)."""
        verify_url = f"https://qualification-verification-system.vercel.app/verify/?code={self.verification_code}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=3,
        )
        qr.add_data(verify_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#002B49", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{b64_str}"

    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.student.full_name}"
