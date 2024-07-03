# yearbook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('student/new/', views.student_create, name='student_create'),  # Correctly define the URL pattern for creating a new student
    path('student/<str:student_id>/', views.student_detail, name='student_detail'),
    path('student/<str:student_id>/edit/', views.student_update, name='student_update'),
    path('student/<str:student_id>/delete/', views.student_delete, name='student_delete'),
]


