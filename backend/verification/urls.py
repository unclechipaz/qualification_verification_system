from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('verify/', views.verify_view, name='verify'),
    path('verify/scan/', views.qr_scanner_view, name='qr_scanner'),
    path('verify/pdf/<int:log_id>/', views.download_verification_pdf, name='download_verification_pdf'),
]
