from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from authentication.permissions import IsEmployer, IsAdminOrRegistrar
from verification.models import VerificationLog
from .models import Employer
from .serializers import EmployerSerializer

@login_required
def employer_portal_view(request):
    """Employer Portal showing Verification History and CSV/PDF export options."""
    if request.user.role != 'EMPLOYER' and not request.user.is_admin_or_registrar():
        messages.error(request, "Employer portal access required.")
        return redirect('dashboard')

    history = VerificationLog.objects.filter(verified_by=request.user).select_related('certificate', 'certificate__student')
    total_performed = history.count()
    verified_count = history.filter(result_status='VERIFIED').count()

    return render(request, 'dashboard/employer_dashboard.html', {
        'history': history,
        'total_performed': total_performed,
        'verified_count': verified_count
    })

class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = [IsAdminOrRegistrar]
