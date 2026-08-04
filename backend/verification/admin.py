from django.contrib import admin
from .models import VerificationLog

@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ('search_query', 'search_type', 'result_status', 'verified_by', 'ip_address', 'is_suspicious', 'anomaly_score', 'timestamp')
    list_filter = ('result_status', 'search_type', 'is_suspicious', 'timestamp')
    search_fields = ('search_query', 'ip_address', 'fraud_reason')
