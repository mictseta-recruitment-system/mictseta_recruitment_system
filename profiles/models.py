from django.db import models
from django.contrib.auth.models import User
import uuid
from config.models import NQF, LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification, JobTitle

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    idnumber = models.CharField(max_length=13, unique=True)
    phone = models.CharField(max_length=10, null=True, default=" ")
    dob = models.CharField(max_length=6,null=False )
    gender = models.CharField(max_length=6, null=False)
    age = models.CharField(max_length=6, null=False)
    maritial_status = models.CharField(max_length=10, default=" ")
    race = models.CharField(max_length=15, default=" ")
    disability = models.CharField(max_length=30, default=" ")
    is_verified = models.BooleanField(default=False, null=False)
    linkedin_profile = models.CharField(max_length=225, default=" ")
    personal_website = models.CharField(max_length=225, default=" ")
    cover_letter = models.CharField(max_length=225, default=" ")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return f'{self.user.email} Profile Information'

class Language(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	language = models.ForeignKey(LanguageList, on_delete=models.CASCADE)
	reading_proficiency = models.ForeignKey(ReadingProficiencyList, on_delete=models.CASCADE)
	writing_proficiency = models.ForeignKey(WritingProficiencyList, on_delete=models.CASCADE)
	speaking_proficiency = models.ForeignKey(SpeakingProficiencyList, on_delete=models.CASCADE)
	def __str__(self):
		return f" {self.language.name}"

class SoftSkills(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	skill = models.ForeignKey(SoftSkillsList, on_delete=models.CASCADE)
	proficiency = models.ForeignKey(SoftProficiency, on_delete=models.CASCADE)
	def __str__(self):
		return f"{self.user.email} Soft Skills information"

class ComputerSkills(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	skill = models.ForeignKey(ComputerSkillsList, on_delete=models.CASCADE)
	proficiency = models.ForeignKey(ComputerProficiency, on_delete=models.CASCADE)
	
	def __str__(self):
		return f"{self.user.email} Computer Skills information"

class Education(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qualifications')
	institution = models.ForeignKey(Institution, on_delete=models.CASCADE) 
	field_of_study = models.ForeignKey(Qualification, on_delete=models.CASCADE) 
	nqf_level = models.ForeignKey(NQF, on_delete=models.CASCADE) 
	start_date = models.CharField(max_length=225, null=True)
	end_date =  models.CharField(max_length=225, null=True)
	status =  models.CharField(max_length=225, null=True)
	def __str__(self):
		return f"{self.user.email} Qualification information"


class WorkingExpereince(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="working_expereince")
	job_title = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
	company = models.CharField(max_length=225)
	location = models.CharField(max_length=225)
	start_date = models.CharField(max_length=225)
	end_date = models.CharField(max_length=225)
	description = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.company}"
		
	def __repr__(self):
		return f"{self.company}"

class AddressInformation(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
	street_address_line = models.CharField(max_length=225,null=True )
	city = models.CharField(max_length=225,null=True )
	province = models.CharField(max_length=225,null=True)
	postal_code = models.CharField(max_length=6,null=True )
	
	def __str__(self):
		return f"{self.user.email} Address Information"

class Reference(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reference")
	working_experince = models.ForeignKey(WorkingExpereince, on_delete=models.CASCADE, related_name="ref_exp" )
	full_name = models.CharField(max_length=225,null=True )
	phone = models.CharField(max_length=225,null=True)
	position = models.CharField(max_length=60,null=True )	
	def __str__(self):
		return f"{self.working_experince.job_title} refernce"


class ProfileImage(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='static/profiles/images/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.user.email} Profile Image"




class SupportingDocuments(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
	document = models.ImageField(upload_to='static/supportindocuments/documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	document_type = models.CharField(max_length=225, null=False)
	def __str__(self):
		return f"{self.user.email} ID or Drivers Liscence or passport"


	
# =======================================================================================

class StaffProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=50,null=True )
	department = models.CharField(max_length=50,null=True )
	salary = models.CharField(max_length=225,null=True )
	hire_date = models.DateTimeField(auto_now_add=True)
	phone = models.CharField(max_length=10,null=True )
	idnumber =  models.CharField(max_length=13,null=False )
	gender = models.CharField(max_length=6,null=False )
	age = models.CharField(max_length=6,null=False )
	dob = models.CharField(max_length=15,null=False )
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
