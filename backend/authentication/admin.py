from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'organization_name', 'is_verified_employer', 'is_staff')
    list_filter = ('role', 'is_verified_employer', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Attributes', {'fields': ('role', 'national_id', 'phone_number', 'organization_name', 'is_verified_employer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Attributes', {'fields': ('role', 'national_id', 'phone_number', 'organization_name', 'is_verified_employer')}),
    )
