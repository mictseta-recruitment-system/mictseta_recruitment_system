from django import forms
from django.contrib.auth.models import User
import re
# from .models import 
# from authenticate.data_validator import *

class AddJobForm(forms.Form):
	description = forms.CharField()
	job_type = forms.CharField()
	location = forms.CharField(max_length=150)
	salary_range = forms.CharField(max_length=100)
	
	def validate_names(self,name):
		pattern = r"[~`!@#$%^*()=\/\*\\|}{\[\];\?]"
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

	def clean_description(self):
		description = self.cleaned_data.get('description')
		return self.validate_names(description)
		
	def clean_job_type(self):
		job_type = self.cleaned_data.get('job_type')
		return self.validate_names(job_type)
	
	def clean_location(self):
		location = self.cleaned_data.get('location')
		return self.validate_names(location)

	def clean_salary_range(self):
		salary_range = self.cleaned_data.get('salary_range')
		return self.validate_names(salary_range)


class AddJobSkillForm(forms.Form):
	level = forms.CharField(max_length=150)
	name = forms.CharField()

	def validate_names(self,name):
		pattern = r"[~`!@#$%^*()=\/\*\\|}{\[\];\?]"
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

	def clean_level(self):
		level = self.cleaned_data.get('level')
		if len(level) > 149 :
			raise forms.ValidationError(f"level is too long")
		return self.validate_names(level)
	
	def clean_name(self):
		name = self.cleaned_data.get('name')
		return self.validate_names(name)
	
class AddJobAcademicForm(forms.Form):
	level = forms.CharField(max_length=150)
	qualification = forms.CharField()

	def validate_names(self,name):
		pattern = r"[~`!@#$%^*()=\/\*\\|}{\[\];\?]"
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

	def clean_level(self):
		level = self.cleaned_data.get('level')
		if len(level) > 149 :
			raise forms.ValidationError(f"level is too long")
		return self.validate_names(level)
	
	def clean_qualification(self):
		qualification = self.cleaned_data.get('qualification')
		return self.validate_names(qualification)

class AddJobExperienceForm(forms.Form):
	name = forms.CharField(max_length=150)
	duration = forms.CharField()

	def validate_names(self,name):
		pattern = r"[~`!@#$%^*()=\/\*\\|}{\[\];\?]"
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

	def clean_name(self):
		name = self.cleaned_data.get('name')
		if len(name) > 149 :
			raise forms.ValidationError(f"name is too long")
		return self.validate_names(name)
	
	def clean_duration(self):
		duration = self.cleaned_data.get('duration')
		try:
			duraton, time = duration.split(" ")
			int(duration)
			str(time)
			return duration
		except:
			return forms.ValidationError('Iconccerct data format try - 2 Month or 8 Years')

class AddJobRequirementForm(forms.Form):
	description = forms.CharField(max_length=150)

	def validate_names(self,name):
		pattern = r"[~`!@#$%^*()=\/\*\\|}{\[\];\?]"
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

	def clean_description(self):
		description = self.cleaned_data.get('description')
		if len(description) > 149 :
			raise forms.ValidationError(f"description is too long")
		return self.validate_names(description)
	
	