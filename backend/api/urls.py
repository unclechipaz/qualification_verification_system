from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import APILoginView, APIRegisterView, UserViewSet
from students.views import StudentViewSet
from qualifications.views import QualificationViewSet, CertificateViewSet
from verification.views import APIVerifyView
from employers.views import EmployerViewSet
from reports.views import APIReportsView
from ai_fraud.views import AIFraudAnalyticsAPIView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='api_users')
router.register(r'students', StudentViewSet, basename='api_students')
router.register(r'qualifications', QualificationViewSet, basename='api_qualifications')
router.register(r'certificates', CertificateViewSet, basename='api_certificates')
router.register(r'employers', EmployerViewSet, basename='api_employers')

urlpatterns = [
    # Auth Endpoints
    path('login/', APILoginView.as_view(), name='api_login'),
    path('register/', APIRegisterView.as_view(), name='api_register'),
    
    # Verification Endpoint
    path('verify/', APIVerifyView.as_view(), name='api_verify'),
    
    # Reports & Analytics Endpoints
    path('reports/', APIReportsView.as_view(), name='api_reports'),
    path('fraud-analytics/', AIFraudAnalyticsAPIView.as_view(), name='api_fraud_analytics'),
    
    # Router ViewSets
    path('', include(router.urls)),
]
