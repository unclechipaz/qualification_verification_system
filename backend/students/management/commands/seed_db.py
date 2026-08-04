import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from students.models import Student
from qualifications.models import Qualification, Certificate
from employers.models import Employer
from verification.models import VerificationLog
from audit.models import AuditLog

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with realistic Midlands State University test data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Applying database migrations..."))
        call_command('migrate', interactive=False)

        self.stdout.write(self.style.SUCCESS("Starting MSU QVS Database Seeding..."))

        # 1. Create Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@msu.ac.zw',
                'first_name': 'Charlton',
                'last_name': 'Ndlovu',
                'role': User.Role.ADMINISTRATOR,
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('AdminPass123!')
        admin_user.save()

        registrar_user, _ = User.objects.get_or_create(
            username='registrar',
            defaults={
                'email': 'registrar@msu.ac.zw',
                'first_name': 'Collen',
                'last_name': 'Simba',
                'role': User.Role.REGISTRAR,
                'is_staff': True
            }
        )
        registrar_user.set_password('RegistrarPass123!')
        registrar_user.save()

        employer_user, _ = User.objects.get_or_create(
            username='employer1',
            defaults={
                'email': 'hr@econet.co.zw',
                'first_name': 'Doreen',
                'last_name': 'Moyo',
                'role': User.Role.EMPLOYER,
                'organization_name': 'Econet Wireless Zimbabwe',
                'is_verified_employer': True
            }
        )
        employer_user.set_password('EmployerPass123!')
        employer_user.save()

        graduate_user, _ = User.objects.get_or_create(
            username='graduate1',
            defaults={
                'email': 'artwell.zimba@gmail.com',
                'first_name': 'Artwell',
                'last_name': 'Zimba',
                'role': User.Role.GRADUATE,
                'national_id': '63-1234567-B-07'
            }
        )
        graduate_user.set_password('GraduatePass123!')
        graduate_user.save()

        self.stdout.write("Created system users (admin, registrar, employer1, graduate1).")

        # 2. Create Qualifications
        q_cs, _ = Qualification.objects.get_or_create(
            code='BSC-CS',
            defaults={
                'title': 'Bachelor of Science Honors Degree in Computer Science',
                'faculty': 'Science and Technology',
                'department': 'Computer Science',
                'duration_years': 4,
                'description': 'Comprehensive program covering software engineering, data structures, cloud computing, and AI.'
            }
        )

        q_acc, _ = Qualification.objects.get_or_create(
            code='BCOM-ACC',
            defaults={
                'title': 'Bachelor of Commerce Honors Degree in Accounting',
                'faculty': 'Commerce',
                'department': 'Accounting',
                'duration_years': 4,
                'description': 'Advanced financial accounting, auditing, taxation, and corporate governance.'
            }
        )

        q_law, _ = Qualification.objects.get_or_create(
            code='LLB-LAW',
            defaults={
                'title': 'Bachelor of Laws Honors Degree (LLB)',
                'faculty': 'Law',
                'department': 'Public and Private Law',
                'duration_years': 5,
                'description': 'Rigorous legal training in jurisprudence, constitutional law, and international law.'
            }
        )

        # 3. Create Students
        students_data = [
            {
                'student_number': 'R201452X',
                'national_id': '63-1234567-B-07',
                'full_name': 'Artwell Zimba',
                'programme': 'BSc Computer Science',
                'faculty': 'Science and Technology',
                'level': Student.Level.UNDERGRADUATE,
                'graduation_date': datetime.date(2024, 11, 20),
                'qualification': q_cs.title,
                'degree_classification': Student.DegreeClassification.FIRST_CLASS,
                'status': Student.Status.GRADUATED,
                'user': graduate_user,
                'qual_obj': q_cs,
                'cert_num': 'MSU-2024-BSC-CS-0001',
                'cert_status': Certificate.Status.ACTIVE
            },
            {
                'student_number': 'R202110Y',
                'national_id': '63-7654321-C-12',
                'full_name': 'Anesu Mutasa',
                'programme': 'BSc Computer Science',
                'faculty': 'Science and Technology',
                'level': Student.Level.UNDERGRADUATE,
                'graduation_date': datetime.date(2024, 11, 20),
                'qualification': q_cs.title,
                'degree_classification': Student.DegreeClassification.UPPER_SECOND,
                'status': Student.Status.GRADUATED,
                'user': None,
                'qual_obj': q_cs,
                'cert_num': 'MSU-2024-BSC-CS-0002',
                'cert_status': Certificate.Status.ACTIVE
            },
            {
                'student_number': 'R198765A',
                'national_id': '63-9988776-D-01',
                'full_name': 'Tinashe Mpofu',
                'programme': 'BCom Accounting',
                'faculty': 'Commerce',
                'level': Student.Level.UNDERGRADUATE,
                'graduation_date': datetime.date(2023, 11, 15),
                'qualification': q_acc.title,
                'degree_classification': Student.DegreeClassification.LOWER_SECOND,
                'status': Student.Status.REVOKED,
                'user': None,
                'qual_obj': q_acc,
                'cert_num': 'MSU-2023-BCOM-ACC-0099',
                'cert_status': Certificate.Status.REVOKED,
                'revocation_reason': 'Academic dishonesty during 4th year thesis examination.'
            },
        ]

        for data in students_data:
            st, _ = Student.objects.get_or_create(
                student_number=data['student_number'],
                defaults={
                    'national_id': data['national_id'],
                    'full_name': data['full_name'],
                    'programme': data['programme'],
                    'faculty': data['faculty'],
                    'level': data['level'],
                    'graduation_date': data['graduation_date'],
                    'qualification': data['qualification'],
                    'degree_classification': data['degree_classification'],
                    'status': data['status'],
                    'user': data['user']
                }
            )

            cert, _ = Certificate.objects.get_or_create(
                student=st,
                defaults={
                    'qualification': data['qual_obj'],
                    'certificate_number': data['cert_num'],
                    'issue_date': data['graduation_date'],
                    'status': data['cert_status'],
                    'revocation_reason': data.get('revocation_reason', '')
                }
            )

        # 4. Create Employer Profile
        Employer.objects.get_or_create(
            user=employer_user,
            defaults={
                'company_name': 'Econet Wireless Zimbabwe',
                'industry': 'Telecommunications & Fintech',
                'contact_person': 'Doreen Moyo (HR Director)',
                'contact_email': 'hr@econet.co.zw',
                'contact_phone': '+263 77 123 4567',
                'is_verified_company': True
            }
        )

        # 5. Create Verification Logs
        c1 = Certificate.objects.get(certificate_number='MSU-2024-BSC-CS-0001')
        c_rev = Certificate.objects.get(certificate_number='MSU-2023-BCOM-ACC-0099')

        VerificationLog.objects.create(
            search_query='MSU-2024-BSC-CS-0001',
            search_type=VerificationLog.SearchType.CERTIFICATE_NUMBER,
            result_status=VerificationLog.ResultStatus.VERIFIED,
            certificate=c1,
            verified_by=employer_user,
            ip_address='197.221.240.10',
            anomaly_score=0,
            is_suspicious=False,
            fraud_reason='Normal Pattern'
        )

        VerificationLog.objects.create(
            search_query='MSU-2023-BCOM-ACC-0099',
            search_type=VerificationLog.SearchType.CERTIFICATE_NUMBER,
            result_status=VerificationLog.ResultStatus.REVOKED,
            certificate=c_rev,
            verified_by=None,
            ip_address='41.223.118.5',
            anomaly_score=60,
            is_suspicious=True,
            fraud_reason='CRITICAL: Attempted verification on REVOKED certificate.'
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded database with MSU test data!"))
