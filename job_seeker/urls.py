from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    path('', views.job_seeker_dashboard, name='jobseeker.dashboard'),
 	# path('add_job/', views.add_job, name='add_job'),
    # path('add_job_skill/', views.add_job_skill, name='add_job_skill'),
]