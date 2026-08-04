from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list_view, name='student_list'),
    path('add/', views.student_create_view, name='student_create'),
]
