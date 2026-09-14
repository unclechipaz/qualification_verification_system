from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ai_fraud.views import AIFraudAnalyticsAPIView
from authentication.views import APILoginView, APIRegisterView, UserViewSet
from employers.views import EmployerViewSet
from qualifications.views import CertificateViewSet, QualificationViewSet
from reports.views import APIReportsView
from students.views import StudentViewSet
from verification.views import APIVerifyView

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
