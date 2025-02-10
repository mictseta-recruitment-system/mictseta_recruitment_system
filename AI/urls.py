from . import views
from django.contrib import admin
from django.urls import path 

urlpatterns = [ 
    path('train_model/', views.train_model, name='train_model'),
 	path('chat/', views.chat_page, name='chat'),
 	path('test_model/',views.test_model, name="test_model")

 	]