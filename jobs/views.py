from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .forms import AddJobForm, AddJobSkillForm ,AddJobAcademicForm, AddJobExperienceForm, AddJobRequirementForm
from .models import JobPost, Academic, Skill, Experience, Requirement
import re
from datetime import datetime

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
				# 'application_deadline' :	json_data.get('application_deadline')            
		}
		jobs.append(job)
	return jobs


@ensure_csrf_cookie
def jobs_home(request):

	return HttpResponse("Welcomt to job posts")





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
				'company_name'	:	json_data.get('company_name')
			}
			for key, value in data.items():

				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
				if key in ['end_date']:
					if " " in value:
						return JsonResponse({'errors':{f'{key}':['spaces not allowed']}, 'status':'error'}, status=404)
			try:
				date_format = "%d:%b:%Y"
				end_date = datetime.strptime(data['end_date'], date_format)
			except:
				return JsonResponse({'errors': 'Iconccerct data format try - DD:MMM:YYYY', 'status':'error'}, status=404)
   
			form = AddJobForm(data)
			if form.is_valid():
				exists = JobPost.objects.filter(title=data['title'], industry=data['industry'], company_name=data['company_name']).exists()
				if exists:
					return JsonResponse({'errors': {'job post':['Job Post already exists']}, 'status': 'error'}, status=400)
				try:
					add_job_post = JobPost.objects.create(user=request.user, title=data['title'],description=data['description'],location=data['location'], salary_range=data['salary_range'], job_type=data['job_type'], industry=data['industry'], company_name=data['company_name'], end_date=end_date)
					add_job_post.save()
					return JsonResponse({'message': 'Job Post Created Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

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

# @csrf_protect
# def add_job(request):
# 	if request.user.is_authenticated:
# 		if request.method == 'POST':
# 			try:
# 				json_data = json.loads(request.body)
# 			except Exception:
# 				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
# 			data = {
# 				'title'			:	json_data.get('title'),
# 				'description'	:	json_data.get('description'),
# 				'end_date'		:	json_data.get('end_date'),
# 				'location'		:	json_data.get('location'),
# 				'salary_range'	:	json_data.get('salary_range'),
# 				'job_type'		:	json_data.get('job_type'),
# 				'industry'		:	json_data.get('industry'),
# 				'company_name'	:	json_data.get('company_name')
# 			}
# 			for key, value in data.items():

# 				if key == None or value == None:
# 					return JsonResponse({'errors': {f'{key}':['this field is required ']}, 'status':'error'}, status=404)
# 				if key in ['end_date']:
# 					if " " in value:
# 						return JsonResponse({'errors':{f'{key}':['spaces not allowed']}, 'status':'error'}, status=404)
# 			try:
# 				date_format = "%d:%b:%Y"
# 				end_date = datetime.strptime(data['end_date'], date_format)
# 			except:
# 				return JsonResponse({'errors': 'Iconccerct data format try - DD:MMM:YYYY', 'status':'error'}, status=404)
   
# 			form = AddJobForm(data)
# 			if form.is_valid():
# 				exists = JobPost.objects.filter(title=data['title'], industry=data['industry'], company_name=data['company_name']).exists()
# 				if exists:
# 					return JsonResponse({'errors': {'job post':['Job Post already exists']}, 'status': 'error'}, status=400)
# 				try:
# 					add_job_post = JobPost.objects.create(user=request.user, title=data['title'],description=data['description'],location=data['location'], salary_range=data['salary_range'], job_type=data['job_type'], industry=data['industry'], company_name=data['company_name'], end_date=end_date)
# 					add_job_post.save()
# 					return JsonResponse({'message': 'Job Post Created Successfully', 'status': 'success'}, status=201)
# 				except Exception as e:
# 					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
# 			else:
# 				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
# 		else:
# 			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
# 	else:
# 		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)

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
					return JsonResponse({'message': 'Job academic transcript updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400).objects.filter(title=data['title'], industry=data['industry'], company_name=data['company_name']).exists()
				

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
					return JsonResponse({'message': 'Job experience updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400).objects.create(user=request.user, title=data['title'],description=data['description'],location=data['location'], salary_range=data['salary_range'], job_type=data['job_type'], industry=data['industry'], company_name=data['company_name'], end_date=end_date)

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
					return JsonResponse({'message': 'Job requirements updated Successfully', 'status': 'success'}, status=201)
				except Exception as e:
					return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400).objects.create(user=request.user, title=data['title'],description=data['description'],location=data['location'], salary_range=data['salary_range'], job_type=data['job_type'], industry=data['industry'], company_name=data['company_name'], end_date=end_date)
