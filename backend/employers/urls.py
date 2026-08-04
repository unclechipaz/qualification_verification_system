from django.urls import path
from . import views

urlpatterns = [
    path('portal/', views.employer_portal_view, name='employer_portal'),
]
