from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .data_validator import *


class UserSignInForm(forms.Form):
	email = forms.EmailField(max_length=254)
	password = forms.CharField(max_length=100)
 

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if ' ' in email :
			raise forms.ValidationError("Spaces not allowed in email")
		if not validate_email(email):
			raise forms.ValidationError("Email in Invalid")
		new_email = email.split('@')
		if len(new_email[0]) < 3:
			raise forms.ValidationError("Email length is Invalid") 
		exist = User.objects.filter(email=email).exists()
		if not exist:
			raise forms.ValidationError("Email is not registerd, try to Create Account")
		return email
	
	def clean_password(self):
		password = self.cleaned_data.get('password')
		email = self.cleaned_data.get('email')
		pattern = r"[~`+=\-/\*\\|}{\[\];'\?.,]"
		matches = re.findall(pattern, password)
		if matches:
			raise forms.ValidationError("Password Format is not allowed")
		return password


class UserSignUpForm(forms.Form):
	username = forms.CharField(max_length=150)
	email = forms.CharField(max_length=150)
	first_name = forms.CharField(max_length=150)
	last_name = forms.CharField(max_length=150)
	idnumber  = forms.CharField(max_length=13)
	phone = forms.CharField(max_length=10)
	password = forms.CharField(max_length=128)


	def validate_names(self,name):
     
		pattern = r"[~`+!@#$%^&*()=\-/\*\\|}{\[\];'\?.,]"
		matches = re.findall(pattern, name)
		if matches:
			raise forms.ValidationError("No special characters allowed")
		if len(name) < 3:
			raise forms.ValidationError(f"Name:{name} is too short")
		try:
			str(name)
		except Exception as e:
			raise forms.ValidationError(e)
		return name

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name')
		return self.validate_names(first_name)

	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name')
		return self.validate_names(last_name)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		exist = User.objects.filter(username=username).exists()
		if exist:
			raise forms.ValidationError(f"Username:{username} is already taken")
		return self.validate_names(username)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if ' ' in email :
			raise forms.ValidationError("Spaces not allowed in email")
		if not validate_email(email):
			raise forms.ValidationError(f"Email: {email} in Invalid")
		new_email = email.split('@')
		if len(new_email[0]) < 3:
			raise forms.ValidationError("Email length is Invalid") 
		exist = User.objects.filter(email=email).exists()
		if exist:
			raise forms.ValidationError(f"Email: {email} is already taken")
		return email

	def clean_password(self):
		
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		first_name = self.cleaned_data.get('first_name') 
		# username = self.cleaned_data.get('username')
		
		
		pattern = r"[~`+=\-/\*\\|}{\[\];'\?.,]"
		matches = re.findall(pattern, password)

		if matches:
			
			raise forms.ValidationError("Password Format is not allowed")
		
		if len(password) < 6:
			raise forms.ValidationError("Password is too short")

		char = [char for char in password if char.isdigit()]
		if len(char) < 1:
			raise forms.ValidationError("Password must contain at least one Number")
		
		if first_name in password: #or username in password:
			raise forms.ValidationError("Password cannot contain username of first name")  
		return password

	def clean_idnumber(self):
		idnumber = self.cleaned_data.get('idnumber')
		validate = ValidateIdNumber(idnumber)
		is_valid = validate.validateSAID()
		if not is_valid:
			raise forms.ValidationError(f"Provide ID Number is not a valid South African ID Number")
		return idnumber