from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(db_index=True, max_length=30, unique=True)),
                ('national_id', models.CharField(db_index=True, max_length=50, unique=True)),
                ('full_name', models.CharField(db_index=True, max_length=150)),
                ('programme', models.CharField(max_length=150)),
                ('faculty', models.CharField(max_length=150)),
                ('level', models.CharField(choices=[('Undergraduate', 'Undergraduate'), ('Postgraduate', 'Postgraduate'), ('Doctorate', 'Doctorate'), ('Diploma', 'Diploma')], default='Undergraduate', max_length=30)),
                ('graduation_date', models.DateField()),
                ('qualification', models.CharField(help_text='e.g. Bachelor of Science Honors Degree in Computer Science', max_length=200)),
                ('degree_classification', models.CharField(choices=[('First Class (1.1)', 'First Class (1.1)'), ('Upper Second (2.1)', 'Upper Second (2.1)'), ('Lower Second (2.2)', 'Lower Second (2.2)'), ('Pass', 'Pass'), ('Distinction', 'Distinction'), ('Merit', 'Merit')], max_length=50)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Graduated', 'Graduated'), ('Revoked', 'Revoked'), ('Suspended', 'Suspended')], default='Graduated', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-graduation_date', 'student_number'],
            },
        ),
    ]
