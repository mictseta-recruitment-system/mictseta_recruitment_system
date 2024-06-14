from . import views
from django.contrib import admin
from django.urls import path 


urlpatterns = [ 
    path('jobs_home/', views.jobs_home, name='jobs_home'),
 	path('add_job/', views.add_job, name='add_job'),
    path('add_job_skill/', views.add_job_skill, name='add_job_skill'),
    path('add_job_acedemic/', views.add_job_acedemic, name='add_job_acedemic'),
    path('add_job_expereince/', views.add_job_expereince, name='add_job_expereince'),
    path('add_job_requirements/', views.add_job_requirements, name='add_job_requirements'),
    path('get_jobs/', views.get_jobs, name='get_jobs')
    
    # path('delete_user/', views.delete_user, name='delete_user')

]