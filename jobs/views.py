from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .forms import AddJobForm, AddJobSkillForm ,AddJobAcademicForm, AddJobExperienceForm, AddJobRequirementForm
from .models import JobPost, Academic, ComputerSkill,SoftSkill, Experience, Requirement,Language, Notification, JobApplication, Interview,FeedBack
from config.models import JobTitle, Industry
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle
from .filters import ApplicationFilter
import re
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
from .custom_decorators import check_leave, change_application_status


# Create your views here.

def serialize_job_post(Jobs):
	jobs = []
	for Job in Jobs:
		job = {
			'issued_by'		:	Job.user.username,
			'title'			:	Job.title,
			'description'	:	Job.description,
			'start_date'		:	Job.start_date,
			'end_date'		:	Job.end_date,
			'location'		:	Job.location,
			'salary_range'	:	Job.salary_range,
			'job_type'		:	Job.job_type,
			'industry'		:	Job.industry,
			'assigned_to'	: 	Job.assigned_to.email
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		jobs.append(job)
	return jobs


def serialize_job_skills(Skills):
	skills = []
	for Skill in Skills:
		skill= {
			'name'		:	Skill.name.skill,
			'level'		:	Skill.level.level,
			'id'		:	Skill.id         
		}
		skills.append(skill)
	return skills

def serialize_job_academics(Academics):
	academics = []
	for Academic_ in Academics:
		academic= {
			'level'		:	Academic_.nqf_level.level,
			'qualification'		:Academic_.field_of_study.name	,
			'id'		:	Academic_.id
			
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		academics.append(academic)
	return academics

def serialize_job_experience(Experiences):
	experiences = []
	for Experience_ in Experiences:
		experience= {
			'name'		:	Experience_.name,
			'duration'		:	Experience_.duration,
			'id'		:	Experience_.id
			
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		experiences.append(experience)
	return experiences

def serialize_job_requirements(Requirements):
	requirements = []
	for Requirement_ in Requirements:
		requirement= {
			'description'		:	Requirement_.description,
			'id'		:	Requirement_.id
			
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		requirements.append(requirement)
	return requirements

def serialize_job_language(Languages):
	languages = []
	for Language_ in Languages:
		requirement= {
			'name'		:	Language_.language.name,
			'reading'		:	Language_.reading_proficiency.proficiency,
			'writing'		:	Language_.writing_proficiency.proficiency,
			'speaking'		:	Language_.speaking_proficiency.proficiency,
			'id'		:	Language_.id
			
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		languages.append(requirement)
	return languages


@ensure_csrf_cookie
def jobs_home(request):

	return HttpResponse("Welcomt to job posts")

@csrf_protect
def job_application(request, jobID):
	if request.user.is_authenticated:
		job = JobPost.objects.filter(id=jobID).first()
		exists = JobApplication.objects.filter(user=request.user, job=job).exists()
		if exists:
			return JsonResponse({'errors': {'Application' : ['Application already exists']}, 'status': 'error'}, status=400)
		new_application = JobApplication.objects.create(user=request.user, job=job, status="pending")
		new_application.save()
		try:
			feed_back = FeedBack(user=request.user,job=new_application.job,message="your application is being processed",status="pending")
			feed_back.save()
		except Exception as e:
			print(e)
		return JsonResponse({'message': 'Job Application submitted successfully', 'status': 'success'}, status=201)
	
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)
	

@check_leave
@csrf_protect
def add_job(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'title'			:	json_data.get('title'),
				'description'	:	json_data.get('description'),
				'end_date'		:	json_data.get('end_date'),
				'location'		:	json_data.get('location'),
				'salary_range'	:	json_data.get('salary_range'),
				'job_type'		:	json_data.get('job_type'),
				'industry'		:	json_data.get('industry'),
				'assigned_to'	:	json_data.get('job_assigned_to')
			}
			for key, value in data.items():

				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
				if key in ['end_date']:
					if " " in value:
						return JsonResponse({'errors':{f'{key}':['spaces not allowed']}, 'status':'error'}, status=404)
			try:

				date_format = "%Y-%m-%d"
				end_date = datetime.strptime(data['end_date'], date_format)
				current_date =datetime.now(None)
				if current_date >= end_date:
					return JsonResponse({'errors': {'Date':'End date cannot be a past or currnt date'}, 'status':'error'}, status=404)
			except Exception as e:
				return JsonResponse({'errors': {'Date':f'{e}'}, 'status':'error'}, status=404)
			industry = Industry.objects.get(id=int(data['industry']))
			title = JobTitle.objects.get(id=int(data['title']))
			form = AddJobForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(title=title, industry=industry).exists()
				if exists:
					return JsonResponse({'errors': {'job post':['Job Post already exists']}, 'status': 'error'}, status=400)
				exist = User.objects.filter(email=data['assigned_to']).exists()
				if not exist:
					return JsonResponse({'errors': {'User':'Assigned user does not exist'}, 'status':'error'}, status=404)
				user = User.objects.get(email=data['assigned_to'])
				try:
					add_job_post = JobPost.objects.create(
						user=request.user,
						assigned_to=user, 
						title=title,
						description=data['description'],
						location=data['location'], 
						salary_range=data['salary_range'], 
						job_type=data['job_type'], 
						industry=industry, 
						end_date=end_date
						)
					add_job_post.save()
					noty = Notification.objects.create(user=request.user, action="Created New Job ad", job_title=add_job_post.title, status=add_job_post.status)
					noty.save()
					return JsonResponse({'message': 'Job Post Created Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def get_jobs(request):
	if request.user.is_authenticated:
		jobs = JobPost.objects.all()
		try:
			jobs = serialize_job_post(jobs)
		except Exception as e:
			return JsonResponse({'errors': {'serialize' : [f'{e}']}, 'status': 'error'}, status=401)
		return JsonResponse({'message': 'Job Lists fetched','jobs':jobs, 'status': 'success'}, status=201)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


#not used
@check_leave
@csrf_protect
def move_to_interview(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			try:
				applicant = JobApplication.objects.get(id=int(json_data.get('appID')))
				applicant.status = "interview"
				applicant.save()
				
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="moved to interview stage",status="Processing")
				feed_back.save()
				return JsonResponse({'message': f'{applicant.user.email} moved to interview stage', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def move_to_shortlist(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			try:
				applicant = JobApplication.objects.get(id=int(json_data.get('appID')))
				applicant.status = "short_list"
				applicant.save()
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="moved to Short-List stage",status="Short-List")
				feed_back.save()
				print(feed_back)
				return JsonResponse({'message': f'{applicant.user.email} moved to short-list stage', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 

@check_leave
@csrf_protect
def auto_shortlist(request):
	if not request.user.is_authenticated:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 
	if not request.method == 'POST':
		return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception:
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
	filters = json_data.get('filter')		
	if filters == "all":
		applications = JobApplication.objects.all()
		applications = ApplicationFilter(applications)
		applications.reset_filter()
		applications.strict_filter_by_incomplete_profile()
		applications.strict_filter_by_experience()
		applications.apply_filter()
	else:
		try:
			filter_id = int(filters)
			applications = JobApplication.objects.filter(job__id=filter_id).all()
			applications = ApplicationFilter(applications)
			applications.reset_filter()
			applications.strict_filter_by_incomplete_profile()
			applications.strict_filter_by_experience()
			applications.apply_filter()
		except Exception as e:
			return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=500)

		
	return JsonResponse({'message': f'{applications.get_total()} applications filtered', 'status': 'success'}, status=201)


@check_leave
@csrf_protect
def approve_interview(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			try:
				applicant = JobApplication.objects.get(id=int(json_data.get('appID')))
				applicant.status ="approved"
				applicant.save()
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="Application successully approved we will contact you",status="approved")
				feed_back.save()
				print(feed_back)
				return JsonResponse({'message': f'{applicant.user.email} Application is approved', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def purge(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				applicants = JobApplication.objects.filter(job__status="closed")
				for applicant in applicants:
					applicant.delete()
				return JsonResponse({'message': ' Applications Purged successfully', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def reject_applicantion(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			try:
				applicant = JobApplication.objects.get(id=int(json_data.get('appID')))
				applicant.status ="rejected"
				applicant.save()
				interview = Interview.objects.get(application=applicant)
				if interview:
					interview.delete()
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="Application Rejected",status="rejected")
				feed_back.save()
				return JsonResponse({'message': f'{applicant.user.email} Application is rejected', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def set_interview(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
				data = {
						"date":json_data.get('date'),
						"start_time" : json_data.get('start_time'),
						"end_time": json_data.get('end_time')
				}
			
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			try:
				date_format = "%Y-%m-%d"
				end_date = datetime.strptime(data['date'], date_format)
				current_date =datetime.now(None)
				if current_date >= end_date:
					return JsonResponse({'errors': {'Date':'Interview date cannot older than the current date'}, 'status':'error'}, status=404)
				time_format = "%H:%M"
				
				start_time = datetime.strptime(data['start_time'], time_format)
				end_time = datetime.strptime(data['end_time'], time_format)
				print(data)
				start_datetime = datetime.combine(end_date, start_time.time())
				print(data)
				end_datetime = datetime.combine(end_date, end_time.time())
				print(data)
				if start_datetime > end_datetime:
					return JsonResponse({'errors': {'Time': 'Interview start time must be earlier than the end time'},'status': 'error'},status=404)
			except Exception as e:
				return JsonResponse({'errors': {'Date':f'Choose the correct date or time'}, 'status':'error'}, status=404)

			try:
				applicant = JobApplication.objects.get(id=int(json_data.get('appID')))
				user = applicant.user 
				exists = Interview.objects.filter(user=user,application=applicant).first()
				if exists:
					return JsonResponse({"errors":{'Interview ':['Applicant aleady set for an interview']}, "status":"error"}, status=400)
				interview = Interview.objects.create(user=user,application=applicant,date=data['date'],start_time=data['start_time'],end_time=data['end_time'])
				interview.save()
				applicant.status = "interview"
				applicant.save()
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="Application set for interview",status="Interview")
				feed_back.save()
				return JsonResponse({'message': ' Interview Scheduled successfully', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


@check_leave
@csrf_protect
def calender_reschedule_interview(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
				data = {
						"id":json_data.get('interviewID'),
						"start_time" : json_data.get('start_time'),
						"end_time": json_data.get('end_time')
				}
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			print(data)
			print('------------------------')
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			try:

				date_format = "%Y-%m-%d"
				end_date = datetime.strptime(data['date'], date_format)
				current_date =datetime.now(None)
				if current_date >= end_date:
					return JsonResponse({'errors': {'Date':'Interview date cannot older than the current date'}, 'status':'error'}, status=404)
				time_format = "%H:%M"
				start_time = datetime.strptime(data['start_time'], time_format)
				end_time = datetime.strptime(data['end_time'], time_format)
				start_datetime = datetime.combine(end_date, start_time.time())
				end_datetime = datetime.combine(end_date, end_time.time())
				if start_datetime > end_datetime:
					return JsonResponse({'errors': {'Time': 'Interview start time must be earlier than the end time'},'status': 'error'},status=404)

			except Exception as e:
				return JsonResponse({'errors': {'Date':f'Choose the correct date'}, 'status':'error'}, status=404)

			try:
				exists = Interview.objects.filter(id=int(json_data.get('interviewID'))).first()
				if not exists:
					return JsonResponse({"errors":{'Interview ':['Interview does not exist']}, "status":"error"}, status=400)
				interview = Interview.objects.get(id=int(json_data.get('interviewID')))
				interview.date = data['date']
				interview.start_time = data['start_time']
				interview.end_time = data['end_time']
				interview.save()
				return JsonResponse({'message': ' Interview rescheduled successfully', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


@check_leave
@csrf_protect
def reschedule_interview(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
				data = {
						"date":json_data.get('date'),
						"start_time" : json_data.get('start_time'),
						"end_time": json_data.get('end_time')
				}
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			try:

				date_format = "%Y-%m-%d"
				end_date = datetime.strptime(data['date'], date_format)
				current_date =datetime.now(None)
				if current_date >= end_date:
					return JsonResponse({'errors': {'Date':'Interview date cannot older than the current date'}, 'status':'error'}, status=404)
				time_format = "%H:%M"
				start_time = datetime.strptime(data['start_time'], time_format)
				end_time = datetime.strptime(data['end_time'], time_format)
				start_datetime = datetime.combine(end_date, start_time.time())
				end_datetime = datetime.combine(end_date, end_time.time())
				if start_datetime > end_datetime:
					return JsonResponse({'errors': {'Time': 'Interview start time must be earlier than the end time'},'status': 'error'},status=404)

			except Exception as e:
				return JsonResponse({'errors': {'Date':f'Choose the correct date'}, 'status':'error'}, status=404)

			try:
				exists = Interview.objects.filter(id=int(json_data.get('interviewID'))).first()
				if not exists:
					return JsonResponse({"errors":{'Interview ':['Interview does not exist']}, "status":"error"}, status=400)
				interview = Interview.objects.get(id=int(json_data.get('interviewID')))
				interview.date = data['date']
				interview.start_time = data['start_time']
				interview.end_time = data['end_time']
				interview.save()
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="Application interview Re-scheduled",status="Interview")
				feed_back.save()
				return JsonResponse({'message': ' Interview rescheduled successfully', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


@check_leave
@csrf_protect
def add_job_skill(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'level'			:	json_data.get('level'),
				'name'	:	json_data.get('name'),
				'job_post_id'	:	json_data.get('job_post_id'),
				'is_required' : json_data.get('is_required')	
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			is_required = False 
			if data['is_required'] == 'true':
				is_required = True

			exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			try:
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				try:
					name = ComputerSkillsList.objects.get(skill=data['name'])
					level = ComputerProficiency.objects.get(level=data['level'])
					exists = ComputerSkill.objects.filter(job_post=job_post, name=name).exists()
					if exists:
						return JsonResponse({'errors': {'Skill':[f'{name} skill already exists exist']}, 'status': 'error'}, status=400)
					skill = ComputerSkill.objects.create(job_post=job_post, level=level, name=name, is_required=is_required )
					skill.save()
				except :
					name = SoftSkillsList.objects.get(skill=data['name'])
					level = SoftProficiency.objects.get(level=data['level'])
					exists = SoftSkill.objects.filter(job_post=job_post, name=name).exists()
					if exists:
						return JsonResponse({'errors': {'Skill':[f'{name} skill already exists']}, 'status': 'error'}, status=400)
					skill = SoftSkill.objects.create(job_post=job_post, level=level, name=name, is_required=is_required)
					skill.save()

				c_skills = ComputerSkill.objects.filter(job_post=job_post)
				s_skills = SoftSkill.objects.filter(job_post=job_post)
				print(c_skills)
				print(s_skills)
				skills = serialize_job_skills(c_skills) + serialize_job_skills(s_skills)
				print(skills)
				return JsonResponse({
					'message': 'Job skills updated Successfully',
					'skills':skills, 
					'status': 'success'
					}, 
					status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def add_job_acedemic(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'level'			:	json_data.get('level'),
				'qualification'	:	json_data.get('qualification'),
				'job_post_id'	:	json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			# form = AddJobAcademicForm(data)
			# else:
			# 	return JsonResponse({"errors"if form.is_valid()::form.errors, "status":"error"}, status=400)
			exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			
			job_post = JobPost.objects.get(id=int(data['job_post_id']))
			level = NQF.objects.get(id=int(data['level']))
			qualification = Qualification.objects.get(id=int(data['qualification']))
			exists = Academic.objects.filter(job_post=job_post,  field_of_study=qualification).exists()
			if exists:
				return JsonResponse({'errors': {'Academic':['requirements already exist']}, 'status': 'error'}, status=400)
			try:
				add_job_academic_post = Academic.objects.create(job_post=job_post, field_of_study=qualification, nqf_level=level)
				add_job_academic_post.save()
				educations = Academic.objects.filter(job_post=job_post)
				return JsonResponse({'message': 'Job academic transcript updated Successfully','educations':serialize_job_academics(educations), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)		

@check_leave
@csrf_protect
def add_job_expereince(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'name'			:	json_data.get('name'),
				'duration'	:	json_data.get('duration'),
				'job_post_id'	:	json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			form = AddJobExperienceForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
				try:
					job_post = JobPost.objects.get(id=int(data['job_post_id']))
					exists = Experience.objects.filter(job_post=job_post,name=data["name"]).exists()
					if exists:
						return JsonResponse({'errors': {'Experience':['Experience already exist']}, 'status': 'error'}, status=400)
					add_job_experience_post = Experience.objects.create(job_post=job_post, name=data["name"], duration=data["duration"])
					add_job_experience_post.save()
					experiences = Experience.objects.filter(job_post=job_post)
					return JsonResponse({'message': 'Job experience updated Successfully','experiences':serialize_job_experience(experiences), 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect				
def add_job_requirements(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'description'			:	json_data.get('description'),
				'job_post_id'	:	json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			form = AddJobRequirementForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
				try:
					job_post = JobPost.objects.get(id=int(data['job_post_id']))
					add_job_reqiurements_post = Requirement.objects.create(job_post=job_post, description=data['description'])
					add_job_reqiurements_post.save()
					requirements = Requirement.objects.filter(job_post=job_post)
					return JsonResponse({'message': 'Job requirements updated Successfully','requirements':serialize_job_requirements(requirements), 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect				
def add_job_language(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'language'			:	json_data.get('language'),
				'speaking'			:	json_data.get('speaking'),
				'reading'			:	json_data.get('reading'),
				'writing'			:	json_data.get('writing'),
				'job_post_id'	:	json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			#form = AddJobRequirementForm(data)
			# if form.is_valid():
			# else:
			# 	return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
			exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			language = LanguageList.objects.get(id=int(data['language']))
			speaking = SpeakingProficiencyList.objects.get(id=int(data['speaking']))
			reading = ReadingProficiencyList.objects.get(id=int(data['reading']))
			writing = WritingProficiencyList.objects.get(id=int(data['writing']))

			try:
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				exists = Language.objects.filter(job_post=job_post, language=language).exists()
				print(exists)
				if exists:
					return JsonResponse({'errors': {'Language':['requirement already exist']}, 'status': 'error'}, status=400)
				add_job_language_post = Language.objects.create(job_post=job_post, language=language,reading_proficiency=reading,writing_proficiency=writing,speaking_proficiency=speaking)
				print(add_job_language)
				add_job_language_post.save()
				languages = Language.objects.filter(job_post=job_post)
				return JsonResponse({'message': 'Language updated Successfully','languages':serialize_job_language(languages), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

#=============================================================================================================================================
@check_leave
@csrf_protect
def update_job(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'title'			:	json_data.get('title'),
				'description'	:	json_data.get('description'),
				'end_date'		:	json_data.get('end_date'),
				'location'		:	json_data.get('location'),
				'salary_range'	:	json_data.get('salary_range'),
				'job_type'		:	json_data.get('job_type'),
				'industry'		:	json_data.get('industry'),
				'job_id'	:	json_data.get('job_id'),
				'assigned_to'	:	json_data.get('assigned_to')
			}
			for key, value in data.items():

				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
				if key in ['end_date']:
					if " " in value:
						return JsonResponse({'errors':{f'{key}':['spaces not allowed']}, 'status':'error'}, status=404)
			try:
				date_format = "%Y-%m-%d"
				end_date = datetime.strptime(data['end_date'], date_format)
				current_date =datetime.now(None)
				if current_date >= end_date:
					return JsonResponse({'errors': {'Date':'End date cannot be a past or currnt date'}, 'status':'error'}, status=404)
			except:
				return JsonResponse({'errors': {'Date':['Iconccerct data format try - MM:DD:YYYY']}, 'status':'error'}, status=404)
			industry = Industry.objects.get(id=int(data['industry']))
			title = JobTitle.objects.get(id=int(data['title']))
			form = AddJobForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(id=int(data['job_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job does not exists']}, 'status': 'error'}, status=400)
				exist = User.objects.filter(email=data['assigned_to']).exists()
				if not exist:		
					return JsonResponse({'errors': {'User':'Assigned user does not exist'}, 'status':'error'}, status=404)
				user = User.objects.get(email=data['assigned_to'])
				try:
					update_job_post = JobPost.objects.get(id=int(data['job_id']))
					update_job_post.title = title
					update_job_post.description = data['description']
					update_job_post.end_date = data['end_date']
					update_job_post.location = data['location']
					update_job_post.salary_range = data['salary_range']
					update_job_post.job_type = data['job_type']
					update_job_post.industry = industry

					update_job_post.assigned_to = user
					update_job_post.save()
					return JsonResponse({'message': 'Job Post UPDATED Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def update_job_skill(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'level'			:	json_data.get('level'),
				'name'	:	json_data.get('name'),
				'job_skill_id'	:	json_data.get('job_skill_id')

				
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
   
			form = AddJobSkillForm(data)
			if form.is_valid():
				exists = Skill.objects.filter(id=int(data['job_skill_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Skills does not exist']}, 'status': 'error'}, status=400)
				try:
					job_skill = Skill.objects.get(id=int(data['job_skill_id']))
					job_skill.name = data['name']
					job_skill.level = data['level']
					job_skill.save()
					return JsonResponse({'message': 'Job skills updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400).objects.filter(title=data['title'], industry=data['industry'], company_name=data['company_name']).exists()


@csrf_protect
def update_job_acedemic(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'level'			:	json_data.get('level'),
				'qualification'	:	json_data.get('qualification'),
				'job_academic_id'	:	json_data.get('job_academic_id')

			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			form = AddJobAcademicForm(data)
			if form.is_valid():
				exists = Academic.objects.filter(id=int(data['job_academic_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Adademic transcrript does not exist']}, 'status': 'error'}, status=400)
				try:
					job_academic = JobPost.objects.get(id=int(data['job_academic_id']))
					job_academic.level = data['level']
					job_academic.qualification = data['qualification'] 
					job_academic.save()
					return JsonResponse({'message': 'Job academic transcript updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@csrf_protect
def update_job_expereince(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'name'			:	json_data.get('name'),
				'duration'	:	json_data.get('duration'),
				'job_experience_id'	:	json_data.get('job_experience_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)

			form = AddJobExperienceForm(data)
			if form.is_valid():
				exists = Experience.objects.filter(id=int(data['job_experience_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
				try:
					experience_post = Experience.objects.get(id=int(data['job_experience_id']))
					experience_post.name = data['name']
					experience_post.duration = data['duration']
					add_job_experience_post.save()
					return JsonResponse({'message': 'Job experience updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@csrf_protect				
def update_job_requirements(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'description'			:	json_data.get('description'),
				'job_requirement_id'	:	json_data.get('job_requirement_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)

			form = AddJobRequirementForm(data)
			if form.is_valid():
				exists = Requirement.objects.filter(id=int(data['job_requirement_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
				try:
					requirements_post = Requirement.objects.get(id=int(data['job_requirement_id']))
					requirements_post.description = data['description']
					requirements_post.save()
					return JsonResponse({'message': 'Job requirements updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


#==============================================================================================================================================================================
@check_leave
@csrf_protect
def delete_job(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_id'	:	json_data.get('job_id'),
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
				if key in ['end_date']:
					if " " in value:
						return JsonResponse({'errors':{f'{key}':['spaces not allowed']}, 'status':'error'}, status=404)
			exists = JobPost.objects.filter(id=int(data['job_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job does not exists']}, 'status': 'error'}, status=400)
			try:
				update_job_post = JobPost.objects.get(id=int(data['job_id']))
				update_job_post.delete()
				noty = Notification.objects.create(user=request.user, action="Delete Job Post", job_title=update_job_post.title, status="Deleted")
				noty.save()
				return JsonResponse({'message': 'Job Post removed Successfully', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def delete_job_skill(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_skill_id'	:	json_data.get('job_skill_id'),
				'job_post_id'	:	json_data.get('job_post_id')	
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
   
			job_post = JobPost.objects.get(id=int(data['job_post_id']))
			try:
				name = ComputerSkillsList.objects.get(skill=data['job_skill_id'])
				exists = ComputerSkill.objects.filter(job_post=job_post, name=name).exists()
				if not exists:
					return JsonResponse({'errors': {'Skill':[f'{name} skill already exists exist']}, 'status': 'error'}, status=400)
				job_skill = ComputerSkill.objects.get(name=name)
				job_skill.delete()
			except Exception as e:
				name = SoftSkillsList.objects.get(skill=data['job_skill_id'])
				exists = SoftSkill.objects.filter(job_post=job_post, name=name).exists()
				if not exists:
					return JsonResponse({'errors': {'Skill':[f'{name} skill already exists']}, 'status': 'error'}, status=400)
				job_skill = SoftSkill.objects.get(name=name)
				job_skill.delete()

			job_post = JobPost.objects.get(id=int(data['job_post_id']))
			c_skills = ComputerSkill.objects.filter(job_post=job_post)
			s_skills = SoftSkill.objects.filter(job_post=job_post)
			skills = serialize_job_skills(c_skills) + serialize_job_skills(s_skills)
			return JsonResponse({'message': 'Job skills remved Successfully','skills':skills , 'status': 'success'}, status=201)

				
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400).objects.filter(title=data['title'], industry=data['industry'], company_name=data['company_name']).exists()

@check_leave
@csrf_protect
def delete_job_acedemic(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_academic_id'	:	json_data.get('job_academic_id'),
				'job_post_id'		: json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			
			exists = Academic.objects.filter(id=int(data['job_academic_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Adademic transcrript does not exist']}, 'status': 'error'}, status=400)
			try:
				job_academic = Academic.objects.get(id=int(data['job_academic_id']))
				job_academic.delete()
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				educations = Academic.objects.filter(job_post=job_post)
				return JsonResponse({'message': 'Job academic transcript updated Successfully','educations':serialize_job_academics(educations), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def delete_job_expereince(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_experience_id'	:	json_data.get('job_experience_id'),
				'job_post_id' : json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
	
			exists = Experience.objects.filter(id=int(data['job_experience_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			try:
				experience_post = Experience.objects.get(id=int(data['job_experience_id']))
				experience_post.delete()
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				experiences = Experience.objects.filter(job_post=job_post)
				return JsonResponse({'message': 'Job experience updated Successfully','experiences':serialize_job_experience(experiences), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect				
def delete_job_requirements(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_requirement_id'	:	json_data.get('job_requirement_id'),
				'job_post_id' : json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
	
			exists = Requirement.objects.filter(id=int(data['job_requirement_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			try:
				requirements_post = Requirement.objects.get(id=int(data['job_requirement_id']))
				requirements_post.delete()
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				requirements = Requirement.objects.filter(job_post=job_post)

				return JsonResponse({'message': 'Job requirements updated Successfully','requirements':serialize_job_requirements(requirements), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect
def delete_language(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_language_id'	:	json_data.get('job_language_id'),
				'job_post_id'		: json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
			
			exists = Language.objects.filter(id=int(data['job_language_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Adademic transcrript does not exist']}, 'status': 'error'}, status=400)
			try:
				language = Language.objects.get(id=int(data['job_language_id']))
				language.delete()
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				languages = Language.objects.filter(job_post=job_post)
				return JsonResponse({'message': 'language  updated Successfully','languages':serialize_job_language(languages), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


@check_leave
@csrf_protect	
def complete_job(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_post_id' : json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
	
			exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			try:
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				job_post.is_complete = True
				job_post.status = "pending" 
				job_post.save()
				noty = Notification.objects.create(user=request.user, action="Submitted Job for Approval", job_title=job_post.title.title, status=job_post.status)
				noty.save()
				return JsonResponse({'message': 'Job Post submitted. waiting approval by Land Mananger', 'status': 'success'}, status=200)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

@check_leave
@csrf_protect	
def approve_job(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			data = {
				'job_post_id' : json_data.get('job_post_id')
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
	
			exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
			try:
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				job_post.is_approved = True
				job_post.status = "open"
				job_post.save()
				noty = Notification.objects.create(user=request.user, action="Job Approval", job_title=job_post.title, status=job_post.status)
				noty.save()
				return JsonResponse({'message': 'Job Post approved successfully', 'status': 'success'}, status=200)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)