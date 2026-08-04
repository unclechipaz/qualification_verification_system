from django.contrib import admin
from .models import Qualification, Certificate

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'faculty', 'department', 'duration_years')
    search_fields = ('title', 'code', 'faculty')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'student', 'qualification', 'issue_date', 'status')
    list_filter = ('status', 'issue_date', 'qualification')
    search_fields = ('certificate_number', 'verification_code', 'student__student_number', 'student__full_name')
