from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'target', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'action')
    search_fields = ('user__username', 'action', 'target', 'ip_address', 'details')
