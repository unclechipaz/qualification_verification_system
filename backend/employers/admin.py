from django.contrib import admin
from .models import Employer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'contact_email', 'contact_phone', 'is_verified_company')
    list_filter = ('is_verified_company',)
    search_fields = ('company_name', 'contact_person', 'contact_email')
