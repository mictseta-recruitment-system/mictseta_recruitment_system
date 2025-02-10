from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    path('train_model/', views.train_model, name='train_model'),
 	path('chat/', views.chat_page, name='chat'),
 	path('chat_live/',views.chat_live, name="chat_live")

 	]