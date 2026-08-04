from django.urls import path
from . import views

urlpatterns = [
    path('', views.qualification_list_view, name='qualification_list'),
    path('certificate/<str:cert_number>/', views.certificate_detail_view, name='certificate_detail'),
]
