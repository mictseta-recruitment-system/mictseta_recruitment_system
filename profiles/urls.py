from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    # path('', views.user_profile, name='user_profile'),
    path('', views.render_profile_page, name='render_profile_page'),
    path('update/profile_information/', views.update_user_profile, name='update_user_profile'),
    path('update/personal_information/', views.update_personal_info, name='update_personal_info'),
    path('update/address_information/', views.update_address_info, name='update_address_info'),
    path('update/upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('update/update_staff/', views.update_staff, name='update_staff'),
    path('add/add_staff/', views.add_staff, name='add_staff'),
    path('add/leave/', views.leave, name='leave'),
    path('add/approve_leave/<leaveID>/', views.approve_leave, name='approve_leave'),
    path('add/reject_leave/<leaveID>/', views.reject_leave, name='reject_leave'),
    path('add/seen_leave/<leaveID>/', views.seen_leave, name='seen_leave'),
    path('add/close_leave/<leaveID>/', views.close_leave, name='close_leave'),

    
    # path('', views.home, name='home')
    # path('', views.home, name='home')
] 
