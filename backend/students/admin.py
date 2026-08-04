from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_number', 'full_name', 'national_id', 'programme', 'faculty', 'graduation_date', 'status')
    list_filter = ('faculty', 'level', 'degree_classification', 'status')
    search_fields = ('student_number', 'national_id', 'full_name', 'programme')
