from . import views
from django.contrib import admin
from django.urls import path 


urlpatterns = [ 
    path('', views.panel, name='dashboard.panel'),
    path('view_staff/', views.view_staff, name='dashboard.view_staff'),
    path('add_job/', views.add_job, name='dashboard.add_job'),
    path('update_job/', views.update_job, name='dashboard.update_job'),
    path('view_jobs/', views.view_jobs, name='dashboard.view_jobs'),
    path('job_details/<jobID>/', views.job_details, name="dashboard.job_details"),
    path('get_notifications/', views.get_notifications, name="dashboard.get_notifications"),
    path('delete_notifications/<notID>/', views.delete_notifications, name="dashboard.delete_notifications"),
    path('add_staff_page/', views.add_staff_page, name="dashboard.add_staff_page"),
    path('update_staff/<staffID>/', views.update_staff, name="dashboard.update_staff"),
    path('employee_details/<empID>/', views.employee_details, name="dashboard.employee_details"),
    path('manage_leave/', views.manage_leave, name="dashboard.manage_leave"),
    path('view_leave/', views.view_leave, name="dashboard.view_leave"),
    path('emp_panel/', views.emp_panel, name="dashboard.emp_panel"),
   # path('manage_attendance/', views.manage_attendance, name="dashboard.manage_attendance"),
    path('backup_database/', views.backup_database, name="dashboard.backup_database"),
    path('backup_db/', views.backup_db, name="dashboard.backup_db"),
    path('delete_db/<int:dbID>/', views.delete_db, name="dashboard.delete_db"),
    path('restore_db/<int:dbID>/', views.restore_db, name="dashboard.restore_db"),
    path('task_manager/', views.task_manager, name="dashboard.task_manager"),
    path('crud_events/', views.crud_events, name="dashboard.crud_events"),
    path('login_events/', views.login_events, name="dashboard.login_events"),
    path('job_applications/', views.job_applications, name="dashboard.job_applications"),
    path('calender/', views.calender, name="dashboard.calender"),
    path('edit_job/<jobID>', views.edit_job, name="dashboard.edit_job"),
    
    
    path('jobsekeer_details/<seekerID>/<jobID>', views.jobsekeer_details, name="dashboard.jobsekeer_details"),
    path('filter_job_application/<int:jobID>', views.filter_job_application, name='filter_job_application'),
    path('attendance/report/pdf/', views.attendance_generate_pdf_report, name='dashboard.attendance_generate_pdf_report'),
    path('leave/report/pdf/', views.leave_generate_pdf_report, name='dashboard.leave_generate_pdf_report'),
    path('login_events/report/pdf/', views.login_events_generate_pdf_report, name='dashboard.login_events_generate_pdf_report'),
    path('crud_events/report/pdf/', views.crud_events_generate_pdf_report, name='dashboard.crud_events_generate_pdf_report'),

    path('new_quiz/<job_id>', views.new_quiz, name="dashboard.new_quiz"),
    path('quiz_results/<int:quiz_id>/<int:user_id>/<int:application_id>/', views.quiz_results, name="dashboard.quiz_results"),
   



    
]
