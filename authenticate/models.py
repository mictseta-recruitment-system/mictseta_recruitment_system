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
    is_verified = models.BooleanField(default=False, null=False)

    def __str__(self):

        return f'{self.user.username} Profile Information'

class PersonalInformation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	linkedin_profile = models.CharField(max_length=225)
	personal_website = models.CharField(max_length=225)
	job_title = models.CharField(max_length=225) 
	current_employer =  models.CharField(max_length=225, null=False)
	years_of_expreince = models.CharField(max_length=100, null=False)
	industry = models.CharField(max_length=225, null=False)
	carear_level = models.CharField(max_length=225, null=False)
	desired_job = models.CharField(max_length=225, null=False)
	job_location = models.CharField(max_length=225,null=True )

	def __str__(self):
		return f"{self.user.username} Personal Information"

class AddressInformation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	street_address_line = models.CharField(max_length=225,null=False )
	street_address_line = models.CharField(max_length=225,null=True )
	city = models.CharField(max_length=225,null=False )
	province = models.CharField(max_length=225,null=False)
	postal_code = models.CharField(max_length=6,null=False )
	
	def __str__(self):
		return f"{self.user.username} Address Information"

