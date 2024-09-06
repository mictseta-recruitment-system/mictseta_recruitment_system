from django.urls import path

from . import views
 

urlpatterns = [
    path('auth/sign-in/',views.sign_in,name="api_sign_in"),
    path('auth/sign-up/',views.sign_up,name="api_sign_up"),
    path('auth/log-out/',views.log_out,name="api_log_out"),
    path('auth/reset-password/<uidb64>/<token>/',views.reset_password,name="reset_password"),
    path('jobs/', views.get_all_jobs, name='get_all_jobs'),
    path('jobs/apply/<int:jobID>/', views.apply_for_job, name='apply_for_job'),
]
