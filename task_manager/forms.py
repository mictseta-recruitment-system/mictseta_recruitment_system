from django import forms
import re

class TaskForm(forms.Form):
	name = forms.CharField(max_length=150)
	priority = forms.CharField(max_length=150)
	description = forms.CharField(max_length=252)

	
	def validate_names(self,name):
		pattern = r"[~`!#$%^&*()=\/\*\\|}{\[\];'\?]"
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
		
		return self.validate_names(name)

	def clean_last_name(self):
		priority = self.cleaned_data.get('priority')
		if ' ' in priority :
			raise forms.ValidationError("Spaces not allowed in Task priority")
		return self.validate_names(priority)

	def clean_description(self):
		description = self.cleaned_data.get('description')
		
		return self.validate_names(description)

class CategoryForm(forms.Form):
	name = forms.CharField(max_length=150)

	def validate_names(self,name):
		pattern = r"[~`+!@#$%^&*()=\/\*\\|}{\[\];'\?]"
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
		if ' ' in name :
			raise forms.ValidationError("Spaces not allowed in Category name")
		return self.validate_names(name)