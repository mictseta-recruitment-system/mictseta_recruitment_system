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
    path('manage_attendance/', views.manage_attendance, name="dashboard.manage_attendance"),

    path('attendance/report/pdf/', views.attendance_generate_pdf_report, name='dashboard.attendance_generate_pdf_report'),
    path('leave/report/pdf/', views.leave_generate_pdf_report, name='dashboard.leave_generate_pdf_report'),


    
]
