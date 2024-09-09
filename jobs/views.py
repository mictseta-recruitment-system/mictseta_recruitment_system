from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .forms import AddJobForm, AddJobSkillForm ,AddJobAcademicForm, AddJobExperienceForm, AddJobRequirementForm
from .models import JobPost, Academic, Experience, Notification, JobApplication
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
			'company_name'	:	Job.company_name,
			'assigned_to'	: 	Job.assigned_to.email
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		jobs.append(job)
	return jobs

def serialize_job_academics(Academics):
    academics = []
    for Academic_ in Academics:
        academic = {
            'level': Academic_.level,
            'qualification': Academic_.qualification,
            'field_of_study': Academic_.field_of_study,
            'institution': Academic_.institution,
            'status': Academic_.status,
            'year_obtained': Academic_.year_obtained,
            'transcript': Academic_.transcript.url if Academic_.transcript else None, 
            'id': Academic_.id
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
				'company_name'	:	json_data.get('company_name'),
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
   
			form = AddJobForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(title=data['title'], industry=data['industry'], company_name=data['company_name']).exists()
				if exists:
					return JsonResponse({'errors': {'job post':['Job Post already exists']}, 'status': 'error'}, status=400)
				exist = User.objects.filter(email=data['assigned_to']).exists()
				if not exist:
					return JsonResponse({'errors': {'User':'Assigned user does not exist'}, 'status':'error'}, status=404)
				user = User.objects.get(email=data['assigned_to'])
				try:
					add_job_post = JobPost.objects.create(user=request.user,assigned_to=user, title=data['title'],description=data['description'],location=data['location'], salary_range=data['salary_range'], job_type=data['job_type'], industry=data['industry'], company_name=data['company_name'], end_date=end_date)
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
				return JsonResponse({'message': f'{applicant.user.email} moved to interview stage', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

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


@csrf_protect
def reject_interview(request):
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
				return JsonResponse({'message': f'{applicant.user.email} Application is rejected', 'status': 'success'}, status=201)
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
				'job_post_id'	:	json_data.get('job_post_id')	
			}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
   
			form = AddJobSkillForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
				try:
					job_post = JobPost.objects.get(id=int(data['job_post_id']))
					add_job_academic_post = Skill.objects.create(job_post=job_post, level=data['level'], name=data['name'])
					add_job_academic_post.save()
					skills = Skill.objects.filter(job_post=job_post)
					return JsonResponse({'message': 'Job skills updated Successfully','skills':serialize_job_skills(skills), 'status': 'success'}, status=201)
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
			form = AddJobAcademicForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(id=int(data['job_post_id'])).exists()
				if not exists:
					return JsonResponse({'errors': {'job post':['Job Post does not exist']}, 'status': 'error'}, status=400)
				try:
					job_post = JobPost.objects.get(id=int(data['job_post_id']))
					add_job_academic_post = Academic.objects.create(job_post=job_post, level=data['level'], qualification=data['qualification'])
					add_job_academic_post.save()
					educations = Academic.objects.filter(job_post=job_post)
					return JsonResponse({'message': 'Job academic transcript updated Successfully','educations':serialize_job_academics(educations), 'status': 'success'}, status=201)
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
				'company_name'	:	json_data.get('company_name'),
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
					update_job_post.title = data['title']
					update_job_post.description = data['description']
					update_job_post.end_date = data['end_date']
					update_job_post.location = data['location']
					update_job_post.salary_range = data['salary_range']
					update_job_post.job_type = data['job_type']
					update_job_post.industry = data['industry']
					update_job_post.company_name = data['company_name']
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
   
			
			exists = Skill.objects.filter(id=int(data['job_skill_id'])).exists()
			if not exists:
				return JsonResponse({'errors': {'job post':['Job Skills does not exist']}, 'status': 'error'}, status=400)
			try:
				job_skill = Skill.objects.get(id=int(data['job_skill_id']))
				job_skill.delete()
				print(job_skill)
				job_post = JobPost.objects.get(id=int(data['job_post_id']))
				skills = Skill.objects.filter(job_post=job_post)
				return JsonResponse({'message': 'Job skills remved Successfully','skills':serialize_job_skills(skills), 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
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
				return JsonResponse({'message': 'Job experience updated Successfully','experiences':serialize_job_experiences(experiences), 'status': 'success'}, status=201)
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
				noty = Notification.objects.create(user=request.user, action="Submitted Job for Approval", job_title=job_post.title, status=job_post.status)
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