from rest_framework import serializers
from jobs.models import JobPost, JobApplication

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'   

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'   
