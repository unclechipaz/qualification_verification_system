from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('qualifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_query', models.CharField(max_length=150)),
                ('search_type', models.CharField(choices=[('CERTIFICATE_NUMBER', 'Certificate Number'), ('STUDENT_NUMBER', 'Student Number'), ('VERIFICATION_CODE', 'Verification Code'), ('QR_CODE', 'QR Code Scan'), ('NATIONAL_ID', 'National ID'), ('NAME', 'Student Name')], default='CERTIFICATE_NUMBER', max_length=30)),
                ('result_status', models.CharField(choices=[('VERIFIED', 'Verified / Valid'), ('INVALID', 'Invalid / Not Found'), ('REVOKED', 'Revoked'), ('PENDING', 'Pending Verification')], max_length=20)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, null=True)),
                ('is_suspicious', models.BooleanField(default=False)),
                ('fraud_reason', models.TextField(blank=True, null=True)),
                ('anomaly_score', models.IntegerField(default=0, help_text='0 to 100 Risk Score')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('certificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='verifications', to='qualifications.certificate')),
                ('verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
