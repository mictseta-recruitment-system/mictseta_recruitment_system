from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
   
 	path('chat/', views.chat_page, name='chat'),
 	

 	]