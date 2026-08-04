import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='e.g. Bachelor of Science Honors Degree in Computer Science', max_length=200)),
                ('code', models.CharField(help_text='e.g. BSC-CS', max_length=50, unique=True)),
                ('faculty', models.CharField(max_length=150)),
                ('department', models.CharField(max_length=150)),
                ('duration_years', models.IntegerField(default=4)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_number', models.CharField(db_index=True, max_length=50, unique=True)),
                ('verification_code', models.CharField(db_index=True, default=uuid.uuid4, max_length=64, unique=True)),
                ('issue_date', models.DateField()),
                ('qr_code_image', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active / Valid'), ('REVOKED', 'Revoked'), ('SUSPENDED', 'Suspended')], default='ACTIVE', max_length=20)),
                ('revocation_reason', models.TextField(blank=True, null=True)),
                ('digital_signature_hash', models.CharField(blank=True, max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('qualification', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificates', to='qualifications.qualification')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='certificate', to='students.student')),
            ],
        ),
    ]
