from django.db import models
# Create your models here.


#Language models 
#========================================================================
class LanguageList(models.Model):
	name = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.name}"

class SpeakingProficiencyList(models.Model):
	proficiency = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.proficiency}"

class ReadingProficiencyList(models.Model):
	proficiency = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.proficiency}"

class WritingProficiencyList(models.Model):
	proficiency = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.proficiency}"
#========================================================================



#Computer skills models
#========================================================================
class ComputerSkillsList(models.Model):
	skill = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.skill}"

class ComputerProficiency(models.Model):
	level = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.level}"

#========================================================================


#Soft skills models
#========================================================================
class SoftSkillsList(models.Model):
	skill = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.skill}"

class SoftProficiency(models.Model):
	level = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.level}"
#========================================================================


class Institution(models.Model):
	name = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.name}"

class Qualification(models.Model):
	name = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.name}"

class JobTitle(models.Model):
	title = models.CharField(max_length=225)
	def __str__(self):
		return f"{self.title}"

