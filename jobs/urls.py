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
    path('update_job/', views.update_job, name='update_job'),
    path('update_job_skill/', views.update_job_skill, name='update_job_skill'),
    path('update_job_acedemic/', views.update_job_acedemic, name='update_job_acedemic'),
    path('update_job_expereince/', views.update_job_expereince, name='update_job_expereince'),
    path('update_job_requirements/', views.update_job_requirements, name='update_job_requirements'),
    path('delete_job/', views.delete_job, name='delete_job'),
    path('delete_job_skill/', views.delete_job_skill, name='delete_job_skill'),
    path('delete_job_acedemic/', views.delete_job_acedemic, name='delete_job_acedemic'),
    path('delete_job_expereince/', views.delete_job_expereince, name='delete_job_expereince'),
    path('delete_job_requirements/', views.delete_job_requirements, name='delete_job_requirements'),
    path('complete_job/', views.complete_job, name='complete_job'),
    path('approve_job/', views.approve_job, name='approve_job'),
    path('get_jobs/', views.get_jobs, name='get_jobs'),
    path('job_application/<int:jobID>', views.job_application, name='job_application'),
    path('move_to_interview/', views.move_to_interview, name='move_to_interview'),
    path('move_to_shortlist/', views.move_to_shortlist, name='move_to_shortlist'),
    path('approve_interview/', views.approve_interview, name='approve_interview'),
    path('reject_applicantion/', views.reject_applicantion, name='reject_applicantion'),
    path('purge/', views.purge, name='purge'),
    path('set_interview/', views.set_interview, name='set_interview'),
    path('reschedule_interview/', views.reschedule_interview, name='reschedule_interview'),
    path('calender_reschedule_interview/', views.calender_reschedule_interview, name='calender_reschedule_interview'),


    # path('delete_user/', views.delete_user, name='delete_user')
]