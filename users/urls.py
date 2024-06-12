from . import views
from django.contrib import admin
from django.urls import path 


urlpatterns = [ 
 	path('get_all_users_page/', views.get_all_users_page, name='get_all_users_page'),
    path('get_user/<username>/', views.get_user, name='get_user'),
    path('get_users/', views.get_users, name='get_users'),
    path('delete_user/', views.delete_user, name='delete_user')

]