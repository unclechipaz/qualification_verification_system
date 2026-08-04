from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = 'ADMINISTRATOR', 'Administrator'
        REGISTRAR = 'REGISTRAR', 'Registrar'
        GRADUATE = 'GRADUATE', 'Graduate'
        EMPLOYER = 'EMPLOYER', 'Employer'
        PUBLIC_VERIFIER = 'PUBLIC_VERIFIER', 'Public Verifier'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PUBLIC_VERIFIER,
        help_text="Role-based access control role."
    )
    national_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    organization_name = models.CharField(max_length=150, blank=True, null=True)
    is_verified_employer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_admin_or_registrar(self):
        return self.role in [self.Role.ADMINISTRATOR, self.Role.REGISTRAR] or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
