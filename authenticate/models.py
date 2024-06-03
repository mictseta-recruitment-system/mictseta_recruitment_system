from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class UserProfile(models.Model):
# 	first_name = models.CharField(max_length=100 )
# 	last_name = models.CharField(max_length=100)
# 	email = models.EmailField(max_length=100, unique=True)
# 	id_number = models.CharField(max_length=100, unique=True)
# 	password = models.CharField(max_length=100)
	
# 	def __str__(self):
# 		return f' {self.first_name} {self.last_name} '

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idnumber = models.CharField(max_length=13, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=6, null=True)
    age = models.CharField(max_length=6, null=True)


    def __str__(self):
        return f'{self.user.username} Profile'