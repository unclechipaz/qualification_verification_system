from django.db import models
from django.conf import settings

class Student(models.Model):
    class Level(models.TextChoices):
        UNDERGRADUATE = 'Undergraduate', 'Undergraduate'
        POSTGRADUATE = 'Postgraduate', 'Postgraduate'
        DOCTORATE = 'Doctorate', 'Doctorate'
        DIPLOMA = 'Diploma', 'Diploma'

    class DegreeClassification(models.TextChoices):
        FIRST_CLASS = 'First Class (1.1)', 'First Class (1.1)'
        UPPER_SECOND = 'Upper Second (2.1)', 'Upper Second (2.1)'
        LOWER_SECOND = 'Lower Second (2.2)', 'Lower Second (2.2)'
        PASS = 'Pass', 'Pass'
        DISTINCTION = 'Distinction', 'Distinction'
        MERIT = 'Merit', 'Merit'

    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        GRADUATED = 'Graduated', 'Graduated'
        REVOKED = 'Revoked', 'Revoked'
        SUSPENDED = 'Suspended', 'Suspended'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile'
    )
    student_number = models.CharField(max_length=30, unique=True, db_index=True)
    national_id = models.CharField(max_length=50, unique=True, db_index=True)
    full_name = models.CharField(max_length=150, db_index=True)
    programme = models.CharField(max_length=150)
    faculty = models.CharField(max_length=150)
    level = models.CharField(max_length=30, choices=Level.choices, default=Level.UNDERGRADUATE)
    graduation_date = models.DateField()
    qualification = models.CharField(max_length=200, help_text="e.g. Bachelor of Science Honors Degree in Computer Science")
    degree_classification = models.CharField(max_length=50, choices=DegreeClassification.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.GRADUATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-graduation_date', 'student_number']

    def __str__(self):
        return f"{self.full_name} ({self.student_number})"
