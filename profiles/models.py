from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idnumber = models.CharField(max_length=13, unique=True)
    phone = models.CharField(max_length=10, unique=True, null=True)
    dob = models.CharField(max_length=6,null=False )
    gender = models.CharField(max_length=6, null=True)
    age = models.CharField(max_length=6, null=True)
    maritial_status = models.CharField(max_length=10, null=True)
    race = models.CharField(max_length=15, null=True)
    disability = models.CharField(max_length=30, null=True)
    is_verified = models.BooleanField(default=False, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

    def __str__(self):

        return f'{self.user.email} Profile Information'

class PersonalInformation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
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
		return f"{self.user.email} Personal Information"

class AddressInformation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	street_address_line = models.CharField(max_length=225,null=True )
	street_address_line1 = models.CharField(max_length=225,null=True )
	city = models.CharField(max_length=225,null=True )
	province = models.CharField(max_length=225,null=True)
	postal_code = models.CharField(max_length=6,null=True )
	
	def __str__(self):
		return f"{self.user.email} Address Information"


class ProfileImage(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='static/profiles/images/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.user.email} Profile Image"

	
# =======================================================================================

class StaffProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=100,null=True )
	department = models.CharField(max_length=6,null=True )
	salary = models.CharField(max_length=225,null=True )
	hire_date = models.DateTimeField(auto_now_add=True)
	phone = models.CharField(max_length=6,null=True )
	idnumber =  models.CharField(max_length=13,null=False )
	gender = models.CharField(max_length=6,null=False )
	age = models.CharField(max_length=6,null=False )
	dob = models.CharField(max_length=6,null=False )
	def __str__(self):
		return f"{self.user.email} Staff Profile"

class Shift(models.Model):
	employee = models.OneToOneField(User, on_delete=models.CASCADE)
	rate = models.CharField(max_length=100,null=True )
	start_time = models.CharField(max_length=225,null=False)
	end_time = models.CharField(max_length=225,null=False)
	working_hours = models.CharField(max_length=225,null=False)
	def __str__(self):
		return f"{self.employee.email} Shift Details"
	
	
class Attendance(models.Model):
	employee = models.ForeignKey(User, on_delete=models.CASCADE)
	shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
	minutes = models.CharField(max_length=225,null=True )
	is_late = models.BooleanField(null=False, default=True)
	status = models.CharField(max_length=225,null=False )
	active = models.CharField(max_length=225,null=True, default="Inactive")
	date = models.DateField(auto_now_add=True)
	def __str__(self):
		return f"{self.employee.email} Shift Details"

class Leave(models.Model):
	employee = models.ForeignKey(User, on_delete=models.CASCADE)
	lave_type = models.CharField(max_length=225,null=False )
	message = models.CharField(max_length=225,null=False)
	start_date = models.DateTimeField(null=False)
	end_date = models.DateTimeField(null=False)
	date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=225,null=False )
	seen = models.BooleanField(null=False, default=False)
	def __str__(self):
		return f"{self.employee.email} Leave Details"


class Raise(models.Model):
	employee = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.CharField(max_length=225,null=False)
	amount = models.CharField(max_length=225,null=False)
	date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=225,null=False )
	def __str__(self):
		return f"{self.employee.email} Raise Details"
