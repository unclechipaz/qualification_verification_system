import csv
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.permissions import IsAdminOrRegistrar
from authentication.models import User
from students.models import Student
from qualifications.models import Certificate
from verification.models import VerificationLog
from employers.models import Employer
from audit.models import AuditLog

@login_required
def main_dashboard_view(request):
    """Routing hub directing users to appropriate role-based dashboard."""
    user = request.user
    if user.is_admin_or_registrar():
        return admin_dashboard_view(request)
    elif user.role == 'EMPLOYER':
        return redirect('employer_portal')
    elif user.role == 'GRADUATE':
        return graduate_dashboard_view(request)
    else:
        return redirect('home')

@login_required
def admin_dashboard_view(request):
    """Admin & Registrar Unified Dashboard with real-time statistics."""
    if not request.user.is_admin_or_registrar():
        messages.error(request, "Access denied.")
        return redirect('home')

    total_graduates = Student.objects.filter(status='GRADUATED').count()
    total_certificates = Certificate.objects.count()
    active_certificates = Certificate.objects.filter(status='ACTIVE').count()
    revoked_certificates = Certificate.objects.filter(status='REVOKED').count()
    total_employers = Employer.objects.count()
    total_verifications = VerificationLog.objects.count()
    suspicious_verifications = VerificationLog.objects.filter(is_suspicious=True).count()

    recent_activities = AuditLog.objects.select_related('user').all()[:10]
    recent_verifications = VerificationLog.objects.select_related('certificate').all()[:10]

    context = {
        'total_graduates': total_graduates,
        'total_certificates': total_certificates,
        'active_certificates': active_certificates,
        'revoked_certificates': revoked_certificates,
        'total_employers': total_employers,
        'total_verifications': total_verifications,
        'suspicious_verifications': suspicious_verifications,
        'recent_activities': recent_activities,
        'recent_verifications': recent_verifications,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def graduate_dashboard_view(request):
    """Graduate Dashboard showing own certificate and QR code."""
    student_profile = getattr(request.user, 'student_profile', None)
    certificate = getattr(student_profile, 'certificate', None) if student_profile else None
    
    return render(request, 'dashboard/graduate_dashboard.html', {
        'student': student_profile,
        'certificate': certificate
    })

@login_required
def verification_reports_view(request):
    """Daily, Weekly, Monthly Verification Summary Reports UI."""
    if not request.user.is_admin_or_registrar():
        messages.error(request, "Access denied.")
        return redirect('home')

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0)
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)

    daily_count = VerificationLog.objects.filter(timestamp__gte=today_start).count()
    weekly_count = VerificationLog.objects.filter(timestamp__gte=week_start).count()
    monthly_count = VerificationLog.objects.filter(timestamp__gte=month_start).count()

    # Breakdown by Status
    status_breakdown = VerificationLog.objects.values('result_status').annotate(count=Count('id'))

    return render(request, 'reports/verification_reports.html', {
        'daily_count': daily_count,
        'weekly_count': weekly_count,
        'monthly_count': monthly_count,
        'status_breakdown': status_breakdown
    })

@login_required
def export_verification_csv(request):
    """Export verification logs to CSV."""
    if not request.user.is_admin_or_registrar() and request.user.role != 'EMPLOYER':
        messages.error(request, "Access denied.")
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="MSU_Verification_Logs.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Query', 'Search Type', 'Result Status', 'Timestamp', 'IP Address', 'Is Suspicious', 'Anomaly Score'])

    logs = VerificationLog.objects.all()
    if request.user.role == 'EMPLOYER':
        logs = logs.filter(verified_by=request.user)

    for log in logs:
        writer.writerow([
            log.id, log.search_query, log.search_type, log.result_status,
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'), log.ip_address,
            log.is_suspicious, log.anomaly_score
        ])

    return response

class APIReportsView(APIView):
    permission_classes = [IsAdminOrRegistrar]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0)
        week_start = now - timedelta(days=7)

        return Response({
            'total_students': Student.objects.count(),
            'total_certificates': Certificate.objects.count(),
            'active_certificates': Certificate.objects.filter(status='ACTIVE').count(),
            'revoked_certificates': Certificate.objects.filter(status='REVOKED').count(),
            'total_verifications': VerificationLog.objects.count(),
            'verifications_today': VerificationLog.objects.filter(timestamp__gte=today_start).count(),
            'verifications_this_week': VerificationLog.objects.filter(timestamp__gte=week_start).count(),
            'suspicious_verifications': VerificationLog.objects.filter(is_suspicious=True).count(),
        })
