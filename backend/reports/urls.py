from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.main_dashboard_view, name='dashboard'),
    path('analytics/', views.verification_reports_view, name='reports'),
    path('export/csv/', views.export_verification_csv, name='export_csv'),
]
