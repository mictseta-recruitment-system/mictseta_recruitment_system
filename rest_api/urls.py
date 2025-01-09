from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView 
from . import views

urlpatterns = [  
    path('auth/registration/', RegisterView.as_view(), name='register'), 
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/', LoginView.as_view(), name='login'), 
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('jobs/', views.get_all_jobs, name='get_all_jobs'),
    path('auth/sign-in/',views.sign_in,name="api_sign_in"),
    path('auth/sign-up/',views.sign_up,name="api_sign_up"),
    path('auth/account/verify-email/',views.send_verification_email,name="api_sign_up"), 
    path('jobs/apply/<int:jobID>/', views.apply_for_job, name='apply_for_job'),
   ]


# urlpatterns = [
#     path('auth/sign-in/',views.sign_in,name="api_sign_in"),
#     path('auth/sign-up/',views.sign_up,name="api_sign_up"),
#     path('auth/log-out/',views.log_out,name="api_log_out"),
#     path('auth/reset-password/<uidb64>/<token>/',views.reset_password,name="reset_password"),
#     path('jobs/apply/<int:jobID>/', views.apply_for_job, name='apply_for_job'),
# ]
