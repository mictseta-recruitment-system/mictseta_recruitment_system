from rest_framework import serializers
from jobs.models import JobPost, JobApplication
from django.contrib.auth.models import User

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = '__all__'   

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'   
class UserSerializer(serializers.ModelSerializer):
      
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
 
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        ) 
        user.set_password(validated_data['password'])
        user.save()
        return user
 
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
         
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)   
        instance.save()
        return instance