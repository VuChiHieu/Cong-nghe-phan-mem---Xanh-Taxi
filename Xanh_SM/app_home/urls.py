from django.contrib import admin
from django.urls import include, path
from .import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register_driver/', views.register_driver, name='register_driver'),
    path('driver', views.driver, name='driver'),
    path('driver/edit/<int:driver_id>/', views.edit_driver, name='edit_driver'),
    path('delete/<int:driver_id>/', views.delete_driver, name='delete_driver'),
    path('student/', views.student_list, name='student'),
    path('student/register/', views.register_student, name='register_student'),
    path('student/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:pk>/', views.delete_student, name='delete_student'),
]