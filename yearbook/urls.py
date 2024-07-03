# yearbook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), #TODO ADD HALL OF FAME, GALLERY, CLEAN A BIT
    path('students/', views.student_list, name='student_list'), # NEED TO ADD FILTERS
    path('student/new/', views.student_create, name='student_create'),  # JUST CHECK ABOUT LOGIN
    path('student/<str:student_id>/', views.student_detail, name='student_detail'), # ADD THE IMAGE LATER
    path('student/<str:student_id>/edit/', views.student_update, name='student_update'),
    # path('student/<str:student_id>/delete/', views.student_delete, name='student_delete'),
]


