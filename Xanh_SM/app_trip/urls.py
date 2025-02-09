from django.contrib import admin
from django.urls import include, path
from .import views

urlpatterns = [  
    path('', views.trip, name='trip'),
    path('add/', views.add_trip, name='add_trip'),  
    path('edit/<int:id>/', views.edit_trip, name='edit_trip'), 
    path('delete/<int:id>/', views.delete_trip, name='delete_trip'),
]