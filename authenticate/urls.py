from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 


urlpatterns = [
	path('sign_in/', views.sign_in, name="sign_in"),
	path('log_out/',views.log_out, name="log_out"),
	path('sign_up/', views.sign_up, name="sign_up"),
	path('authenticates/', views.render_auth_page, name='render_auth_page'),
	# path('', views.home, name="home"),
	path('reset_password/<uidb64>/<token>/', views.reset_password, name="reset_password"),
	path('reset_password_link/',views.reset_password_link, name="reset_password_link"),
	path('find_account/',views.find_account, name='find_account'),
	path('reset_link/', views.reset_link, name='reset_link')
]

