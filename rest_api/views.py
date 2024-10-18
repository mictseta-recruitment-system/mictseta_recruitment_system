from rest_framework.decorators import api_view  
from rest_framework import status
from jobs.models import JobPost, JobApplication
from .serializers import JobPostSerializer, JobApplicationSerializer
from django.utils.timezone import now 
from profiles.models import Profile  
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status  
from django.core.mail import send_mail
from django.conf import settings  
from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


 
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def get_user_profile_data(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET': 
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT': 
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
@permission_classes([IsAuthenticated]) 
def apply_for_job(request, jobID):
    user = request.user
     
    if not request.user.is_authenticated:
        return Response({'errors': {'Authentication': ['User is not authenticated']}}, status=status.HTTP_401_UNAUTHORIZED)
    
    job = JobPost.objects.filter(id=jobID).first()

    if not job:
        return Response({'errors': {'Job': ['Job not found']}}, status=status.HTTP_404_NOT_FOUND)

    exists = JobApplication.objects.filter(user=user, job_id=job.id).exists()
    if exists:
        return Response({'errors': {'Application': ['Application already exists']}}, status=status.HTTP_400_BAD_REQUEST)

    new_application = JobApplication.objects.create(user=user, job_id=job.id, status="pending")
    new_application.save()

    send_mail(
        'Application sent successfully',
        'Please note that your application has been sent successfully.',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],  
        fail_silently=False,
    )

    return Response({'message': 'Your Application was submitted successfully'}, status=status.HTTP_201_CREATED)

 