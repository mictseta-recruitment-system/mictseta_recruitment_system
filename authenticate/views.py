from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import UserSignInForm, UserSignUpForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#  Create your views here.
from django.core.mail import send_mail
from django.conf import settings
def send_welcome_email(user_email):
    subject = 'Welcome to Our Website'
    message = 'Thank you for signing up for our website. We are excited to have you!'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    send_mail(subject, message, email_from, recipient_list)

@csrf_exempt
def sign_in(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == "POST":
		try:
			json_data = json.loads(request.body)
		except Exception :
			return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
		email = json_data.get('email')
		password = json_data.get('password')
		data = {
			'email':email,
			'password': password
		}
		
		form = UserSignInForm(data)
		if form.is_valid() :
			user = User.objects.get(email=email)
			user = authenticate(request, username=user.username, password=password)
			print(user)
			if user is not None:
				login(request, user)
				return redirect('home')
				#return JsonResponse({'message':f"Logged in as : {user.username} " , 'status':'success'}, status=200)
			else:
				return JsonResponse({'errors':{'password':['Password is incorrect']}, 'status':'error'}, status=400)
		else:
			return JsonResponse({'errors': form.errors, 'status':'error'}, status=400)

	return render(request, "signin.html")

@csrf_exempt
def sign_up(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body)
		except Exception :
			return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
		data = {
		'username' : json_data.get('username'),
		'first_name' : json_data.get('first_name'),
		'last_name' : json_data.get('last_name'),
		'email' : json_data.get('email'),
		'phone' : json_data.get('phone'),
		'idnumber': json_data.get('idnumber'),
		'password' : json_data.get('password'),
		'password2' : json_data.get('password2')

		}

		form = UserSignUpForm(data)
		
		if form.is_valid():
			if data['password'] != data['password2']:
				return JsonResponse({'errors':{'password':['password no match ']}, 'status':'error'}, status=400)
			
			user = authenticate(request, email=data['email'], password=data['password'])
			if user is None:
				new_user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
				new_user.save()
				return JsonResponse({'message':f'User profile for {new_user.username} is created successfuly', 'status':'success'}, status=201)
		else:
			return JsonResponse({'errors': form.errors, 'status': 'error'}, status=403)
	return render(request, "signup.html")



@csrf_exempt
@login_required(login_url='/auth/sign_in')
def log_out(request):
	logout(request)
	return redirect('sign_in')

@login_required(login_url='/auth/sign_in')
def home(request):
	return render(request,'index.html')