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
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
import json
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse 
import random
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

verification_code = None

@csrf_exempt
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def apply_for_job(request, jobID):
    user = request.user
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({'errors': {'Authentication': ['User is not authenticated']}}, status=status.HTTP_401_UNAUTHORIZED)
    
    job = JobPost.objects.filter(id=jobID).first()

    if not job:
        return Response({'errors': {'Job': ['Job not found']}}, status=status.HTTP_404_NOT_FOUND)

    exists = JobApplication.objects.filter(user=user, job_id=job).exists()
    if exists:
        return Response({'errors': {'Application': ['Application already exists']}}, status=status.HTTP_400_BAD_REQUEST)

    new_application = JobApplication.objects.create(user=user, job_id=job, status="pending")
    new_application.save()
    send_mail(
            'Application sent successfully',
            f'Please note that you application have been sent successfully.',
            settings.DEFAULT_FROM_EMAIL,
            request.user.data['email'],
            fail_silently=False,
        )
    return Response({'message': 'Your Application was submitted successfully'}, status=status.HTTP_201_CREATED)


def send_verification_email(name,email):
    global verification_code
    verification_code = random.randint(100000, 999999)
    
    send_mail(
            'Verify Your Email Address',
            f'Hello {name},We are aware that you a trying to create an account with MICTSETA.\nYour verification code is: {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    return verification_code


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    try: 
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    # global verification_code
    
    if serializer.is_valid():
        # verification_cod= send_verification_email(request.data['username'],request.data['email'])
        # if verification_code==verification_cod:
        serializer.save()
        user = User.objects.get(username=data['username'])
        token = Token.objects.create(user=user)
        idnumber = request.data.get('idnumber')
    
        if idnumber: 
            age = ValidateIdNumber(idnumber).get_age()
            gender = ValidateIdNumber(idnumber).get_gender()
            dob = ValidateIdNumber(idnumber).get_birthdate()

            
            profile, created = Profile.objects.get_or_create(user=user)
            profile.idnumber = idnumber
            profile.age = age
            profile.gender = gender
            profile.dob = dob
            profile.save()
        return Response({"token": token.key, "User": serializer.data})
        # else:
        #     return Response({"Detail":"The verification code is incorrect!"})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['POST'])
@permission_classes([AllowAny])
def sign_in(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({"details": "Email and password required."}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, email=email)
    if not user.check_password(password):
        return Response({"details": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def log_out(request):
    try: 
        token = Token.objects.get(user=request.user)
        token.delete() 
        logout(request)

        return Response({'message': 'Logged out successfully', 'status': 'success'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'errors': 'Token not found, user is not logged in', 'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)