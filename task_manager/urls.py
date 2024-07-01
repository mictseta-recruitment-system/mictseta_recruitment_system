from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    path('create_task/', views.create_task, name='create_task'),
 	path('update_task/', views.update_task, name='update_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('create_category/', views.create_category, name='create_category'),
    path('update_category/', views.update_category, name='update_category'),
    path('delete_category/', views.delete_category, name='delete_category'),
    

    # path('delete_user/', views.delete_user, name='delete_user')

]