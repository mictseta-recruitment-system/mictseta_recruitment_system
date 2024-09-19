from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    # path('', views.user_profile, name='user_profile'),
    path('', views.render_profile_page, name='render_profile_page'),
    path('update/profile_information/', views.update_user_profile, name='update_user_profile'),
    path('update/update_qualification/', views.update_qualification, name='update_qualification'),
    path('update/address_information/', views.update_address_info, name='update_address_info'),
    path('update/language_information/', views.update_language, name='update_language'),
    path('update/computer_skill_information/', views.update_computer_skill, name='update_computer_skill'),
    path('update/soft_skill_information/', views.update_soft_skill, name='update_soft_skill'),
    path('update/upload_supporting_document/', views.upload_supporting_document, name='upload_supporting_document'),
    path('delete/delete_supporting_document/<document_id>/', views.delete_supporting_document, name='delete_supporting_document'),
    path('update/update_working_experince/', views.update_working_experince, name='update_working_experince'),
    
    path('update/upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('update/update_staff/', views.update_staff, name='update_staff'),
    path('add/add_staff/', views.add_staff, name='add_staff'),
    path('add/leave/', views.leave, name='leave'),
    path('add/approve_leave/<leaveID>/', views.approve_leave, name='approve_leave'),
    path('add/reject_leave/<leaveID>/', views.reject_leave, name='reject_leave'),
    path('add/seen_leave/<leaveID>/', views.seen_leave, name='seen_leave'),
    path('add/close_leave/<leaveID>/', views.close_leave, name='close_leave'),
    path('add/mark_attendence/<empID>/', views.mark_attendence, name='mark_attendence'),
    path('add/end_attendace/<empID>/', views.end_attendace, name='end_attendace'),

] 
