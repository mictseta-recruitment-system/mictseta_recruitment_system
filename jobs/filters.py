from django.db.models import Q, Count
from datetime import datetime
from .utils import *


class ApplicationFilter:
	
	def __init__(self,applications):
		self.applications = applications.annotate(
				documents_count=Count('user__documents'), 
				softskills_count=Count('user__softskills') ,
				computerskills_count=Count('user__computerskills'), 
				working_expereince_count=Count('user__working_expereince'),
				language_count=Count('user__language'),
				qualifications_count=Count('user__qualifications'),
				address_count=Count('user__address')
				)
		
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

	def standerd_filter(self):
		self.filter_by_incomplete_profile()
		print("*********  profile filter ********")
		print(self.filterd_apllications)
		self.filter_by_soft_skill()
		print("********* soft skill filter ********")
		print(self.filterd_apllications)
		self.filter_by_computer_skill()
		print("*********  computer skill filter ********")
		print(self.filterd_apllications)
		self.filter_by_academic()
		print("********* academics filter ********")
		print(self.filterd_apllications)
		self.filter_by_language()
		print("*********language filter ********")
		print(self.filterd_apllications)
		self.filter_by_experience()
		print("********* experience filter ********")
		print(self.filterd_apllications)

	
	def strict_filter(self):
		print("\n")
		self.strict_filter_by_incomplete_profile()
		print("********* strict profile filter ********")
		print(self.filterd_apllications)
		self.strict_filter_by_experience()
		print("\n *********strict experience filter ********")
		print(self.filterd_apllications)
		self.strict_filter_by_computer_skill()
		print("\n *********strict  computer skill filter ********")
		print(self.filterd_apllications)
		self.strict_filter_by_soft_skill()
		print("\n *********strict  soft skill filter ********")
		print(self.filterd_apllications)
		self.strict_filter_by_academic()
		print("\n *********strict academics filter ********")
		print(self.filterd_apllications)
		self.filter_by_language()
		print("\n ********* strict language filter ********")
		print(self.filterd_apllications)
		self.strict_filter_by_similarity() 
		print("\n *********strict similarity filter ********")

	def get_exp_years(self, Sdate, Edate):
		date_format = "%Y-%m-%d"
		end_date = datetime.strptime(Edate, date_format)
		start_date = datetime.strptime(Sdate, date_format)

		years_diff = end_date.year - start_date.year
		months_diff = end_date.month - start_date.month
		days_diff = end_date.day - start_date.day
		if months_diff < 0:
		    years_diff -= 1
		    months_diff += 12
		if days_diff < 0:
		    months_diff -= 1
		difference_in_years = years_diff + (months_diff / 12)
		return difference_in_years


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
			Q(user__profile__phone__exact="")|
			Q(user__profile__phone__exact=" ")| 
        
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
				if skill.is_required == True:
					job_skill_list.append(skill.name)
		if len(job_skill_list) > 0:
			valid_applications = self.filterd_apllications.filter(user__computerskills__skill__in=job_skill_list).distinct()
			self.filterd_apllications = valid_applications

	def filter_by_soft_skill(self):
		job_skill_list = []
		for application in self.filterd_apllications:
			for skill in application.job.S_skills.all():
				if skill.is_required == True:
					job_skill_list.append(skill.name)
		if len(job_skill_list) > 0:
			valid_applications = self.filterd_apllications.filter(user__softskills__skill__in=job_skill_list).distinct()
			self.filterd_apllications = valid_applications

	def filter_by_academic(self):
		academic_study_list = []
		academic_level_list = []
		job_experience_list = []  
		for application in self.filterd_apllications:
			if application.job.educations.all():
				job_experience_list.append(application)
		print(job_experience_list)

		print("&%&%&%&%&%&%&%&%&%&%&")
		if job_experience_list:
			for application in self.filterd_apllications:
				for academic in application.job.educations.all():
					academic_study_list.append(academic.field_of_study)
					academic_level_list.append(academic.id)
			valid_applications= self.filterd_apllications.filter(user__qualifications__field_of_study__in=academic_study_list).distinct()
			self.filterd_apllications = valid_applications

	def filter_by_experience(self):
		experience_list = []
		job_experience_list = []  
		for application in self.filterd_apllications:
			if application.job.experiences.all():
				job_experience_list.append(application)
		print(job_experience_list)
		print("&%&%&%&%&%&%&%&%&%&%&")
		if job_experience_list:
			for application in self.filterd_apllications:
				for experience in application.job.experiences.all():
					experience_list.append(experience.name)
			valid_applications= self.filterd_apllications.filter(user__working_expereince__job_title__title__in=experience_list).distinct()
			self.filterd_apllications = valid_applications

	def filter_by_language(self):
		language_list = []
		job_experience_list = []  
		for application in self.filterd_apllications:
			if application.job.j_languages.all():
				job_experience_list.append(application)
		print(job_experience_list)
		print("&%&%&%&%&%&%&%&%&%&%&")
		if job_experience_list:
			for application in self.filterd_apllications:
				for language in application.job.j_languages.all():
					language_list.append(language.language)
			valid_applications= self.filterd_apllications.filter(user__language__language__in=language_list).distinct()
			self.filterd_apllications = valid_applications

	def strict_filter_by_incomplete_profile(self):
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
			Q(user__profile__phone__exact="")|
			Q(user__profile__phone__exact=" ")| 
        
			# Check if race is empty
			Q(user__profile__race__exact="") |
			Q(user__profile__race__exact=" ") |
        
			# Check if marital status is empty
			Q(user__profile__maritial_status__exact="") |
			Q(user__profile__maritial_status__exact=" ") |

			Q(user__profile__disability__exact="") |
			Q(user__profile__disability__exact=" ") |
        	
        	Q(user__profile__race__exact="") |
			Q(user__profile__race__exact=" ") |

			Q(user__profile__linkedin_profile__exact="") |
			Q(user__profile__linkedin_profile__exact=" ") |
        	# Check if no documents are uploaded
			Q(documents_count__lt=1)|
			Q(softskills_count__lt=1)|
			Q(computerskills_count__lt=1)|
			Q(working_expereince_count__lt=1)|
			Q(qualifications_count__lt=1)|
			Q(address_count__lt=1)|
			Q(language_count__lt=1)|

			Q(user__working_expereince__company__exact=" ") |
			Q(user__working_expereince__location__exact=" ") |
			Q(user__working_expereince__description__exact=" ") |
			Q(user__working_expereince__start_date__exact=" ") |
			Q(user__working_expereince__company__exact="") |
			Q(user__working_expereince__location__exact="") |
			Q(user__working_expereince__description__exact="") |
			Q(user__working_expereince__start_date__exact="") 
		).distinct()
    	# Exclude the incomplete users from the original Applications queryset
		self.filterd_apllications = self.applications.exclude(id__in=incomplete_users)
	

	def strict_filter_by_experience(self):
		invalid_applicants = set()
		if self.filterd_apllications:
			for application in self.filterd_apllications:
				job_exps = {exp.name: int(exp.duration) for exp in application.job.experiences.all()}
				user_exps = application.user.working_expereince.all()
				for user_exp in user_exps:
					if user_exp.job_title.title in job_exps:
						user_exp_years = self.get_exp_years(user_exp.start_date, user_exp.end_date)
						if job_exps[user_exp.job_title.title] > user_exp_years:
							invalid_applicants.add(user_exp)
		

	# def strict_filter_by_computer_skill(self):
	# 	job_skill_list = []
	# 	skill_proficiency = {}
	# 	for application in self.filterd_apllications:
	# 		for skill in application.job.C_skills.all().distinct():
	# 			if skill.is_required == True:
	# 				job_skill_list.append(skill.name)
	# 				skill_proficiency[skill.proficiency] = skill.score
	# 	if job_skill_list:
	# 		valid_applications = self.filterd_apllications.filter(user__computerskills__skill__in=job_skill_list, user__computerskills__proficiency__score__gt=skill_proficiency[user__computerskills__proficiency]).distinct()

	# 		self.filterd_apllications = valid_applications



	def strict_filter_by_computer_skill(self):
		job_skill_list = []
		skill_level_score = {}

    # Collect required skills and their scores from the job applications
		for application in self.filterd_apllications:
			for skill in application.job.C_skills.all().distinct():
				if skill.is_required:  # Check if the skill is required
					job_skill_list.append(skill.name.skill)  # Get the skill name
					skill_level_score[skill.name.skill] = skill.level.score  # Map skill name to its score
    # Ensure there are required skills to filter
		skill_temp_score = len(job_skill_list)
		if job_skill_list:
			valid_users = []
			for application in self.filterd_apllications:
				score = 0
				for user_skill in application.user.computerskills_set.all():
					if user_skill.skill.skill in job_skill_list:
						try:
							if user_skill.proficiency.score >= skill_level_score[user_skill.skill.skill]:
								score += 1
						except Exception as e:
							pass
				if score >= skill_temp_score:
					valid_users.append(application.user)
			valid_applications = self.filterd_apllications.filter(user__in=valid_users).distinct()			
			self.filterd_apllications = valid_applications

	def strict_filter_by_soft_skill(self):
		job_skill_list = []
		skill_level_score = {}
   		 # Collect required skills and their scores from the job applications
		for application in self.filterd_apllications:
			for skill in application.job.S_skills.all().distinct():
				if skill.is_required:  # Check if the skill is required
					job_skill_list.append(skill.name.skill)  # Get the skill name
					skill_level_score[skill.name.skill] = skill.level.score  # Map skill name to its score
    	# Ensure there are required skills to filter\
		skill_temp_score = len(job_skill_list)
		if job_skill_list:
			valid_users = []
			for application in self.filterd_apllications:
				score = 0
				for user_skill in application.user.softskills_set.all():
					if user_skill.skill.skill in job_skill_list:
						
						try:
							if user_skill.proficiency.score >= skill_level_score[user_skill.skill.skill]:
								score += 1
						except Exception as e:
							pass
				if score >= skill_temp_score:
					valid_users.append(application.user)
			valid_applications = self.filterd_apllications.filter(user__in=valid_users).distinct()			
			self.filterd_apllications = valid_applications
			
	def strict_filter_by_academic(self):
		academic_study_list = []
		academic_level_list = []
		if self.filterd_apllications:
			for application in self.filterd_apllications:
				for academic in application.job.educations.all():
					academic_study_list.append(academic.field_of_study)
					academic_level_list.append(academic.nqf_level)

			self.filterd_apllications =self.filterd_apllications.exclude(user__qualifications__end_date__exact="In Progress")

	def strict_filter_by_similarity(self):
		threshold_score = 0.80
		users = []
		if self.filterd_apllications:
			for application in self.filterd_apllications:
				user = application.user
				job = application.job

				score = similarity(user.profile.cover_letter,job.description)
				print("\n")
				print(f"threshold score : {threshold_score} ", f"user {user} score : {score}")
				print("\n")
				if score <= threshold_score:
					users.append(user)
			self.filterd_apllications =self.filterd_apllications.exclude(user__in=users)