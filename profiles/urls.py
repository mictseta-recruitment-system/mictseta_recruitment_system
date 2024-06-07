from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    # path('', views.user_profile, name='user_profile'),
    path('', views.render_profile_page, name='render_profile_page'),
    path('update/profile_information/', views.update_user_profile, name='update_user_profile'),
    path('update/personal_information/', views.update_personal_info, name='update_personal_info'),
    #path('update/address_information/', views.update_address_info, name='update_address_info')
    # path('', views.home, name='home')
] 
