from django import forms
from django.contrib.auth.models import User
from profiles.models import Profile
from .data_validator import *


class UserSignInForm(forms.Form):
	email = forms.EmailField(max_length=254)
	password = forms.CharField(max_length=100)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if ' ' in email :
			raise forms.ValidationError("Spaces not allowed in email")
		if not validate_email(email):
			raise forms.ValidationError(" in Invalid")
		new_email = email.split('@')
		if len(new_email[0]) < 3:
			raise forms.ValidationError(" length is Invalid") 
		exist = User.objects.filter(email=email).exists()
		if not exist:
			raise forms.ValidationError("is not registerd, try to Create Account")
		return email
	
	def clean_password(self):
		password = self.cleaned_data.get('password')
		email = self.cleaned_data.get('email')
		pattern = r"[~`+=\-/\*\\|}{\[\];'\?.,]"
		matches = re.findall(pattern, password)
		if matches:
			raise forms.ValidationError(" Format is not allowed")
		return password


class UserSignUpForm(forms.Form):
	
	email = forms.CharField(max_length=150)
	idnumber  = forms.CharField(max_length=13)
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

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if ' ' in email :
			raise forms.ValidationError("Spaces not allowed ")
		if not validate_email(email):
			raise forms.ValidationError(f": {email} in Invalid")
		new_email = email.split('@')
		if len(new_email[0]) < 3:
			raise forms.ValidationError(" length is Invalid") 
		exist = User.objects.filter(email=email).exists()
		if exist:
			raise forms.ValidationError(f"Email: {email} is already taken")
		return email

	def clean_password(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2') 
		username = self.cleaned_data.get('username')
		pattern = r"[~`+=\-/\*\\|}{\[\];'\?.,]"
		matches = re.findall(pattern, password)

		if matches:		
			raise forms.ValidationError(" Format is not allowed")

		if ' ' in password :
			raise forms.ValidationError("Spaces not allowed ")

		if len(password) < 6:
			raise forms.ValidationError(" is too short")

		char = [char for char in password if char.isdigit()]
		if len(char) < 1:
			raise forms.ValidationError(" must contain at least one Number")
		try:
			if username in password: #or username in password:
				raise forms.ValidationError(" cannot contain username ")  
		except:
			pass
		return password


	def clean_idnumber(self):
		idnumber = self.cleaned_data.get('idnumber')
		validate = ValidateIdNumber(idnumber)
		is_valid = validate.validateSAID()
		exist = User.objects.filter(profile__idnumber=idnumber).exists()
		if exist:
			raise forms.ValidationError("Id Number Already taken")
		
		if ' ' in idnumber :
			raise forms.ValidationError("Spaces not allowed ")

		if not is_valid:
		 	raise forms.ValidationError("Provide ID Number is not a valid South African ID Number")
		return idnumber

