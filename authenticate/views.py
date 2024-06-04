from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import UserSignInForm, UserSignUpForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .data_validator import ValidateIdNumber

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

#  Create your views here.
# from django.core
# .mail import send_mail
# from django.conf import settings
# def send_welcome_email(user_email):
#     subject = 'Welcome to Our Website'
#     message = 'Thank you for signing up for our website. We are excited to have you!'
#     email_from = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [user_email]
    
#     send_mail(subject, message, email_from, recipient_list)

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
				new_user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password'], first_name=data['first_name'], last_name=data['last_name'])
				new_user.save()

				profile = Profile.objects.create(user=new_user, idnumber=data['idnumber'], phone=data['phone'], age=ValidateIdNumber(data['idnumber']).get_age(), gender=ValidateIdNumber(data['idnumber']).get_gender() )
				profile.save()
				return JsonResponse({'message':f'User profile for {new_user.username} is created successfuly', 'status':'success'}, status=201)
		else:
			return JsonResponse({'errors': form.errors, 'status': 'error'}, status=403)
	return render(request, "signup.html")



@csrf_exempt
@login_required(login_url='/auth/sign_in')
def log_out(request):
	logout(request)
	return redirect('sign_in')


def home(request):
	return render(request,'index.html')

@csrf_exempt
def reset_password_link(request):
	if request.method == "POST":
		data = request.POST
		email = data['email']
		user = User.objects.get(email=email)
		
		if user:
			token = default_token_generator.make_token(user)
			reset_link = f"http://127.0.0.1:8000/auth/reset_password/{user.id}/{token}/"
			return render(request, 'reset_link.html', {'link':reset_link})
		else:
			return HttpResponse("you dont have an acciunt with us")
	return render(request, 'reset_password_link.html')


@csrf_exempt
def reset_password(request, uidb64, token):
	try:
		uid = int(uidb64)
		user = User.objects.get(pk=uid)
	
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		if request.method == 'POST':
			data = request.POST
			password = data['password']
			re_password = data['re-password']
			print(re_password)
			if password != re_password:
				return render(request, 'reset_password.html')
			else:	
				user.password = password
				user.save()
				return render(request,'complete_reset.html')
	return render(request, 'reset_password.html')