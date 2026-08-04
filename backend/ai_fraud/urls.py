from django.urls import path
from . import views

urlpatterns = [
    path('analytics/', views.fraud_analytics_view, name='fraud_analytics'),
]
