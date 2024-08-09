from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    path('about_us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('job_details/', views.job_details, name='job_details'),
    path('', views.home, name='home')
] 
