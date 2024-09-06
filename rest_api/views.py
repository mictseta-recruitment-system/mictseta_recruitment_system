from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from rest_framework import status
from jobs.models import JobPost, JobApplication
from .serializers import JobPostSerializer, JobApplicationSerializer
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from authenticate.data_validator import ValidateIdNumber
from django.contrib.auth.models import User
from profiles.models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str  
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@api_view(['POST'])
def reset_password(request, uidb64, token):
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(profile__uuid=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
 
    if user is not None and default_token_generator.check_token(user, token):
        try:
            json_data = json.loads(request.body)
        except Exception:
            return Response({'errors': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

        password = json_data.get('new_password')
        re_password = json_data.get('new_password2')
 
        if password != re_password:
            return Response({'errors': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
 
        user.password = make_password(password)
        user.save()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)

    return Response({'errors': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET'])
def get_all_jobs(request):
    current_time = now()
    jobs = JobPost.objects.filter(is_approved=True)
    for job in jobs:
        if job.status != "closed" and current_time > job.end_date:
            job.status = "closed"
            job.save()
    open_jobs = JobPost.objects.filter(status="open")
    serializer = JobPostSerializer(open_jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
 
@api_view(['POST'])
@login_required
def apply_for_job(request, jobID):
    user = request.user
    job = JobPost.objects.filter(id=jobID).first()

    if not job:
        return Response({'errors': {'Job': ['Job not found']}}, status=status.HTTP_404_NOT_FOUND)

    exists = JobApplication.objects.filter(user=user, job_id=job).exists()
    if exists:
        return Response({'errors': {'Application': ['Application already exists']}}, status=status.HTTP_400_BAD_REQUEST)

    new_application = JobApplication.objects.create(user=user, job_id=job, status="pending")
    new_application.save()

    return Response({'message': 'Your Application was submitted successfully'}, status=status.HTTP_201_CREATED)
import json

@api_view(['POST'])
def sign_in(request):
    if request.user.is_authenticated:
        return Response({'message': f"Already logged in as {request.user.username}", 'status': 'warning'}, status=status.HTTP_200_OK)

    try:
        json_data = json.loads(request.body)
    except Exception:
        return Response({'errors': 'Supply a valid JSON object: check documentation for more info', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    email = json_data.get('email')
    password = json_data.get('password')
 
    if not email or not password:
        return Response({'errors': 'Email and password are required', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
 
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'errors': 'User not found', 'status': 'error'}, status=status.HTTP_404_NOT_FOUND)

    user = authenticate(request, username=user.username, password=password)

    if user is not None:
        login(request, user)
        user_type = 'Staff member' if user.is_staff else 'Job Seaker'
        return Response({'message': f'Welcome back {user.username}', 'status': 'success', 'user_type': user_type}, status=status.HTTP_200_OK)
    else:
        return Response({'errors': 'Invalid email or password', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def sign_up(request):
    if request.user.is_authenticated:
        return Response({'message': 'Already logged in', 'status': 'warning'}, status=status.HTTP_200_OK)

    try:
        json_data = json.loads(request.body)
    except Exception:
        return Response({'errors': 'Supply a valid JSON object: check documentation for more info', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    email = json_data.get('email')
    password = json_data.get('password') 
    idnumber = json_data.get('idnumber')
 
    if not email or not password or not idnumber:
        return Response({'errors': 'All fields are required!', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
 
    
    if User.objects.filter(email=email).exists():
        return Response({'errors': 'Email already exists', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
 
    new_user = User.objects.create_user(email=email, password=password, username=idnumber)
    profile = Profile.objects.create(
        user=new_user,
        idnumber=idnumber,
        age=ValidateIdNumber(idnumber).get_age(),
        gender=ValidateIdNumber(idnumber).get_gender(),
        dob=ValidateIdNumber(idnumber).get_birthdate()
    )
    profile.save()

    return Response({'message': f'User profile for {new_user.username} created successfully', 'status': 'success'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'message': 'Logged out successfully', 'status': 'success'}, status=status.HTTP_200_OK)
    else:
        return Response({'errors': 'You are not logged in', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)