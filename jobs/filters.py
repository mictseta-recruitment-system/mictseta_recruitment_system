from django.db.models import Q, Count

class ApplicationFilter:
	
	def __init__(self,applications):
		self.applications = applications.annotate(documents_count=Count('user__documents'))
		self.filterd_apllications = None
		self.total = 0
	def apply_filter(self):
		self.total = 0
		for application in self.filterd_apllications:
			application.filterd_out = True
			application.save()
			self.total += 1
	def reset_filter(self):
		for application in self.applications:
			application.filterd_out = False
			application.save()

	def get_total(self):
		return self.total

	def filter_by_incomplete_profile(self):
    	# Filter applications where the profile is incomplete
		incomplete_users = self.applications.filter(
        	# Check if first or last name is empty
			Q(user__first_name__exact="") |
			Q(user__first_name__exact=" ") |
			Q(user__last_name__exact="") |
			Q(user__last_name__exact=" ") |
        
			# Check if cover letter is less than 10 characters
			Q(user__profile__cover_letter__lt=10) |
        
			# Check if phone is missing or invalid (less than 9 digits)
			Q(user__profile__phone__isnull=True) |
			Q(user__profile__phone__lt=9) |
        
			# Check if race is empty
			Q(user__profile__race__exact="") |
			Q(user__profile__race__exact=" ") |
        
			# Check if marital status is empty
			Q(user__profile__maritial_status__exact="") |
			Q(user__profile__maritial_status__exact=" ") |
        
        	# Check if no documents are uploaded
			Q(documents_count__lt=1)
		).distinct()

    	# Exclude the incomplete users from the original Applications queryset
		self.filterd_apllications = self.applications.exclude(id__in=incomplete_users)

	def filter_by_computer_skill(self):
		job_skill_list = []
		for application in self.filterd_apllications:
			for skill in application.job.C_skills.all().distinct():
				job_skill_list.append(skill.name)
		valid_applications = self.filterd_apllications.filter(user__computerskills__skill__in=job_skill_list).distinct()
		self.filterd_apllications = valid_applications

	def filter_by_soft_skill(self):
		job_skill_list = []
		for application in self.filterd_apllications:
			for skill in application.job.S_skills.all():
				job_skill_list.append(skill.name)
		valid_applications = self.filterd_apllications.filter(user__softskill__skill__in=job_skill_list).distinct()
		self.filterd_apllications = valid_applications

