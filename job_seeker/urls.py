from . import views
from django.urls import path

urlpatterns = [
    path('job_seeker_dashboard', views.job_seeker_dashboard, name='job_seeker_dashboard'), 
    path('personal_details/', views.personal_details, name='personal_details'),
     path('address_details/', views.address_details, name='address_details'),
    path('academic_qualifications/', views.academic_qualifications, name='academic_qualifications'),
    path('language_proficiency/', views.language_proficiency, name='language_proficiency'),
    path('soft_skills/', views.soft_skills, name='soft_skills'),
    path('computer_skills/', views.computer_skills, name='computer_skills'),
    path('working_experience/', views.working_experience, name='working_experience'),
    path('referees/', views.referees, name='referees'),
    path('supporting_documents/', views.supporting_documents, name='supporting_documents'),
    path('job_detail/', views.job_details, name='jobseeker.job_details'),
    path('application_tracking/', views.application_tracking, name='application_tracking'),
    path('interviews/', views.interviews, name='interviews'),
    path('feedback/', views.feedback, name='feedback'),
    path('logout/', views.logout, name='logout'),
    path('job_information/<int:jobID>', views.job_information, name='job_information'),
]
