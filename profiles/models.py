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
    linkedin_profile = models.CharField(max_length=225)
    personal_website = models.CharField(max_length=225)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

    def __str__(self):

        return f'{self.user.email} Profile Information'

class Qualification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qualifications')
	highest_qualification = models.CharField(max_length=225, null=True)
	field_of_study = models.CharField(max_length=225, null=True)
	institution = models.CharField(max_length=225,null=True) 
	year_obtained =  models.CharField(max_length=225, null=True)
	status =  models.CharField(max_length=225, null=True)
	grade = models.CharField(max_length=100, null=True)
	def __str__(self):
		return f"{self.user.email} Qualification information"

class Language(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
	language = models.CharField(max_length=225)
	proficiency = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.user.email} Language and proficiency information"

class ComputerSkills(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
	skill = models.CharField(max_length=225)
	level = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.user.email} Computer Skills information"

class SoftSkills(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	skill = models.CharField(max_length=225)
	level = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.user.email} Soft Skills information"

class WorkingExpereince(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=225)
	company = models.CharField(max_length=225)
	location = models.CharField(max_length=225)
	start_date = models.CharField(max_length=225)
	end_date = models.CharField(max_length=225)
	years_of_expreince = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.user.email} Working Expereince information"

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
