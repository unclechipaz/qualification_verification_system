from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets, filters
from authentication.permissions import IsAdminOrRegistrar
from verification.utils import mask_national_id
from .models import Student
from .serializers import StudentSerializer

# Web UI Views
@login_required
def student_list_view(request):
    if not request.user.is_admin_or_registrar():
        messages.error(request, "Access denied. Registrar or Admin permissions required.")
        return redirect('dashboard')

    query = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(student_number__icontains=query) |
            Q(national_id__icontains=query) |
            Q(full_name__icontains=query) |
            Q(programme__icontains=query)
        )

    # Attach presentation masked_national_id to each student (FR-SRCH-07)
    for student in students:
        student.masked_national_id = mask_national_id(student.national_id)

    return render(request, 'students/student_list.html', {
        'students': students,
        'query': query
    })

@login_required
def student_create_view(request):
    if not request.user.is_admin_or_registrar():
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        national_id = request.POST.get('national_id')
        full_name = request.POST.get('full_name')
        programme = request.POST.get('programme')
        faculty = request.POST.get('faculty')
        level = request.POST.get('level')
        graduation_date = request.POST.get('graduation_date')
        qualification = request.POST.get('qualification')
        degree_classification = request.POST.get('degree_classification')
        status = request.POST.get('status', Student.Status.GRADUATED)

        if Student.objects.filter(student_number=student_number).exists():
            messages.error(request, f"Student number {student_number} already exists.")
            return render(request, 'students/student_form.html')

        student = Student.objects.create(
            student_number=student_number,
            national_id=national_id,
            full_name=full_name,
            programme=programme,
            faculty=faculty,
            level=level,
            graduation_date=graduation_date,
            qualification=qualification,
            degree_classification=degree_classification,
            status=status
        )
        messages.success(request, f"Student {student.full_name} registered successfully!")
        return redirect('student_list')

    return render(request, 'students/student_form.html')

# DRF ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrRegistrar]
    filter_backends = [filters.SearchFilter]
    search_fields = ['student_number', 'national_id', 'full_name', 'programme']
