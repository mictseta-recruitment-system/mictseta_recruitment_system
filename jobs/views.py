from django.shortcuts import render,get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .forms import AddJobForm, AddJobSkillForm ,AddJobAcademicForm, AddJobExperienceForm, AddJobRequirementForm
from .models import JobPost, Academic, ComputerSkill,SoftSkill, Experience, Requirement,Language, Notification, JobApplication, Interview,FeedBack,QuizResults,Quiz,Question,Answer, QuizAnswers,Alert,Scoreboard, ScoreQuestion,ScoreResult
from config.models import JobTitle, Industry
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle
from .filters import ApplicationFilter
import re
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
from .custom_decorators import check_leave, change_application_status
from django.core.mail import send_mail
from django.conf import settings


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
		new_application = JobApplication.objects.create(user=request.user, job=job, status="pending", current_stage="initial stage", reason="initial stage")
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
					noty = Notification.objects.create(user=request.user, action="Created New Job ad", job_title=data['title'], status=add_job_post.status)
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
def requisition(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
   
    jobID = json_data.get('job_post_id')
    print(jobID)
    vacancy = JobPost.objects.get(id=int(jobID))
    vacancy.current_step += 1
    vacancy.save()
    alert = Alert.objects.create(note="Vacancy submitted for Requsition Approval", vacancy=vacancy, step=vacancy.current_step, status="pending")
    alert.save()
    return JsonResponse({'message': 'Vacancy submitted for requisition approval', 'status': 'success'}, status=201)

@check_leave
@csrf_protect
def approve_requisition(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
   
    jobID = json_data.get('job_post_id')
    print(jobID)
    vacancy = JobPost.objects.get(id=int(jobID))
    vacancy.req_finance_approval = True
    vacancy.save()
    alert = Alert.objects.get(vacancy=vacancy, step=2)
    alert.completed = True
    alert.save()
    
    return JsonResponse({'message': 'Requisition Approved, Submitted to CEO', 'status': 'success'}, status=201)

@check_leave
@csrf_protect
def approve_requisition_ceo(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
   
    jobID = json_data.get('job_post_id')
    print(jobID)
    vacancy = JobPost.objects.get(id=int(jobID))
    if vacancy.req_finance_approval:
    	vacancy.req_ceo_approval = True
    	vacancy.current_step += 1
    	vacancy.save()
    else:
    	return JsonResponse({'errors': { "Missing step" : ['Finance must approve first']}, 'status':'error'}, status=403)

    alert = Alert.objects.create(note="Requisition Approved, Prepare Vacancy for Advertisment", vacancy=vacancy, step=vacancy.current_step, status="pending")
    alert.save()
    return JsonResponse({'message': 'Requisation Approved by ceo', 'status': 'success'}, status=201)

@check_leave
@csrf_protect
def screening(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
   
    jobID = json_data.get('job_post_id')
    vacancy = JobPost.objects.get(id=int(jobID))
    vacancy.current_step += 1
    vacancy.save()
    alert = Alert.objects.filter(vacancy=vacancy, step=4).first()
    alert.status = "approved"
    alert.save()
    alert = Alert.objects.create(note="Vacancy Approved for Screening and Nomination", vacancy=vacancy, step=vacancy.current_step, status="pending")
    alert.save()
    return JsonResponse({'message': 'Vacancy Approved for Screening and Nomination', 'status': 'success'}, status=201)

@check_leave
@csrf_protect
def submit_short_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    jobid = json_data.get('jobID')
    vacancy = JobPost.objects.filter(id=int(jobid)).first()
    #applications = JobApplication.filter(vacancy=vacancy,status="short_list").all()
    vacancy.current_step += 1
    vacancy.save()
    alert = Alert.objects.filter(vacancy=vacancy, step=4).first()
    alert.status = "approved"
    alert.save()
    alert = Alert.objects.create(note="Shortlisted Candidates approved", vacancy=vacancy, step=vacancy.current_step, status="completed")
    alert.save()
    return JsonResponse({'message': 'Shortlist submitted', 'status': 'success'}, status=201)

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
				applicant.previous_stage = "short list stage"
				applicant.current_stage = "inteveiw stage"
				applicant.staff = request.user

				applicant.save()
				
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message="moved to interview stage",status="Processing")
				feed_back.save()
				send_mail(
			        'Updated Application Status',
			        'Dear Applicant. \n Your application was successfully moved to the <h1><b>Interview Stage </b></h1> \n kindly check your application tracking status to stay updated \n Best Regards \n MICT SETA',
			        settings.DEFAULT_FROM_EMAIL,
			        ['221649921@edu.vut.ac.za','sixskies25@gmail.com'],  
			        fail_silently=False,
			    )
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
				applicant.previous_stage = applicant.current_stage
				applicant.current_stage = "short listing stage"
				applicant.staff = request.user
				applicant.is_rejected = False 
				applicant.filterd_out = True 
				applicant.reason = ""
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
def auto_move_to_shortlist(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception:
				return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
			try:
				jobID = json_data.get('jobID')
				job = JobPost.objects.filter(id=int(jobID)).first()
				if job :
					for applicant in job.jobapplication_set.all():
						if applicant.status == "pending":
							applicant.status = "short_list"
							applicant.previous_stage = "auto filtering stage"
							applicant.current_stage = "short listing stage"
							applicant.staff = request.user
							applicant.save()
							feed_back = FeedBack.objects.create(user=applicant.user,job=job,message="moved to Short-List stage",status="Short-List")
							feed_back.save()
							print(feed_back)
				return JsonResponse({'message': f'all moved to short-list stage', 'status': 'success'}, status=201)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)

		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 

@check_leave
@csrf_protect
def auto_filter(request):
	if not request.user.is_authenticated:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 
	if not request.method == 'POST':
		return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception:
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
	filters = json_data.get('filter')	
	mode = json_data.get('mode')	
	if filters == "all":
		applications = JobApplication.objects.filter(status="pending")
		applications = ApplicationFilter(applications)
		if mode == "strict":
			applications.reset_filter()
			applications.strict_filter()
			applications.apply_filter()
		if mode == "standerd":
			applications.reset_filter()
			applications.standerd_filter()
			applications.apply_filter()
		if mode not in ['strict','standerd']:
			return JsonResponse({'errors': {'method':['Invalid filter mode']}, 'status': 'error'}, status=400)
	else:
		try:
			filter_id = int(filters)
			applications = JobApplication.objects.filter(job__id=filter_id).all()
			applications = ApplicationFilter(applications)
			applications.reset_filter()
			if mode == "strict":
				applications.reset_filter()
				applications.strict_filter()
			if mode == "standerd":
				applications.reset_filter()
				applications.standerd_filter()
			applications.apply_filter()
		except Exception as e:
			return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=500)

	job_post = JobPost.objects.get(id=filters)
	job_post.is_filter = True
	job_post.save()		
	return JsonResponse({'message': f'{applications.get_total()} applications filtered', 'status': 'success'}, status=201)


@check_leave
@csrf_protect
def apply_filter(request):
	if not request.user.is_authenticated:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 
	if not request.method == 'POST':
		return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception:
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
	filters = json_data.get('filter')	
	

	filter_id = int(filters)
	applications = JobApplication.objects.filter(job__id=filter_id).all()
	for application in applications:
		application.is_filter_applied = True
		application.save()
		feed_back_exist = FeedBack.objects.filter(user=application.user,job=application.job,message=f"{application.reason}",status="rejected").first()
		if not application.filterd_out:
			application.is_rejected = True
			application.save()

			if not feed_back_exist:
				feed_back = FeedBack.objects.create(user=application.user,job=application.job,message=f"{application.reason}",status="rejected")
				feed_back.save() 
		
	return JsonResponse({'message': f'Filter applied  successfully', 'status': 'success'}, status=201)


@check_leave
@csrf_protect
def hide_filter(request):
	if not request.user.is_authenticated:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 
	if not request.method == 'POST':
		return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception:
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
	jobID = json_data.get('jobID')	
	
	job_id = int(jobID)
	job = JobPost.objects.filter(id=job_id).first()
	job.hide_application = True
	job.save()
	print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
	print(job)
	applications = JobApplication.objects.filter(job__id=job_id).all()
	for application in applications:
		if application.is_filter_applied:
			application.hide = True
			application.save()
	return JsonResponse({'message': f'hide applications', 'status': 'success'}, status=201)

@check_leave
@csrf_protect
def show_filter(request):
	if not request.user.is_authenticated:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 
	if not request.method == 'POST':
		return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception:
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
	jobID = json_data.get('jobID')	
	
	job_id = int(jobID)
	job = JobPost.objects.filter(id=job_id).first()
	job.hide_application = False
	job.save()
	applications = JobApplication.objects.filter(job__id=job_id).all()
	for application in applications:
		if application.is_filter_applied:
			application.hide = False
			application.save()
	return JsonResponse({'message': f'show applications', 'status': 'success'}, status=201)

@check_leave
@csrf_protect
def reset_filter(request):
	if not request.user.is_authenticated:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400) 
	if not request.method == 'POST':
		return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception:
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
	jobID = json_data.get('jobID')	
	
	job_id = int(jobID)
	applications = JobApplication.objects.filter(job__id=job_id).all()
	for application in applications:
		if not application.is_filter_applied:
			application.hide = False
			application.filterd_out = False
			application.is_filter = False
			application.reason=""
			application.save()
	return JsonResponse({'message': f'show applications', 'status': 'success'}, status=201)


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
				applicant.previous_stage = "interview stage"
				applicant.current_stage = "approved stage"
				applicant.staff = request.user
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
				applicant.previous_stage = applicant.current_stage
				applicant.current_stage = "rejected stage"
				applicant.staff = request.user
				applicant.is_rejected = True
				applicant.filterd_out = False
				applicant.reason = json_data.get('reason')
				applicant.save()
				interview = Interview.objects.filter(application=applicant).first()
				if interview:
					interview.delete()
				feed_back = FeedBack.objects.create(user=applicant.user,job=applicant.job,message=f"Application Rejected due to {json_data.get('reason')}",status="rejected")
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
				applicant.previous_stage = applicant.current_stage
				applicant.current_stage = "interview stage"
				applicant.staff = request.user
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
def auto_set_interview(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
				data = {
						jobID: json_data.get('jobID')
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
				applicant.previous_stage = applicant.current_stage
				applicant.current_stage = "interview stage"
				applicant.staff = request.user
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
				if update_job_post.is_active:
					update_job_post.is_active = False
					print('working')
					update_job_post.status = "closed"
					print("updated job pust to closed")
				else:
					update_job_post.is_active = True
					update_job_post.status = "open"
					print("updated job pust to open")
				update_job_post.save()
				noty = Notification.objects.create(user=request.user, action="Delete Job Post", job_title=update_job_post.title.title, status="Deleted")
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
				return JsonResponse({'errors': {'Skill':[f'{e} ']}, 'status': 'error'}, status=400)

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
				alert = Alert.objects.create(note="Vacancy submitted for Advertisment Approval", vacancy=job_post, step=job_post.current_step, status="approved")
				alert.save()
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
				job_post.current_step += 1
				job_post.save()
				noty = Notification.objects.create(user=request.user, action="Vacancy Approved for Advertisment", job_title=job_post.title.title, status=job_post.status)
				noty.save()
				alert = Alert.objects.create(note="Vacancy Approved for Advertisment, accepting applications", vacancy=job_post, step=job_post.current_step, status="pending")
				alert.save()
				return JsonResponse({'message': 'Job Post approved successfully', 'status': 'success'}, status=200)
			except Exception as e:
				return JsonResponse({"errors":{'server error':[f'{e}']}, "status":"error"}, status=400)
			
		else:
			return JsonResponse({'errors': {'method':['Invalid request method']}, 'status': 'error'}, status=400)
	else:
		return JsonResponse({'errors': {'authentication' : ['you are not logged in']}, 'status': 'error'}, status=400)


@check_leave
@csrf_protect	
def add_quiz(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'quiz' : json_data.get('quiz'),
    	'job_id' : json_data.get('job_id')
    }
    print(data)
    if  not data['quiz'] or data['quiz'] == "":
    	return JsonResponse({'errors':{ "Error" : ['Quiz name can not be empty']}, 'status':'error'})

    exists = JobPost.objects.filter(id=int(data['job_id'])).first()
    if not exists:
    	return JsonResponse({'errors':'Selected job does not exist', 'status':'error'})

    quiz_exists = Quiz.objects.filter(job=exists, staff=request.user).first()
    if quiz_exists:
    	quiz_exists.title=data['quiz']
    	quiz_exists.save()
    else:
    	quiz = Quiz.objects.create(title=data['quiz'], job=exists, staff=request.user)
    	quiz.save()
    return JsonResponse({'message': 'Quiz Updated successfully', 'status': 'success'}, status=200)

@check_leave
@csrf_protect	
def delete_quiz(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'quiz' : 'quiz_id'
    }

    if not data['quiz'] or data['quiz'] != "":
    	return JsonResponse({'errors':'Quiz name can not be empty', 'status':'error'})

    quiz = Quiz.objects.filter(id=int(data['quiz_id'])).first()
    if not quiz:
    	return JsonResponse({'errors':'Selected job does not exist', 'status':'error'})
    quiz.delete()
    
    return JsonResponse({'message': 'Quiz added successfully', 'status': 'success'}, status=200)


@check_leave
@csrf_protect	
def add_quesion(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'question' : json_data.get('question'),
    	'quiz' : json_data.get('quiz_id')
    }

    if not data['quiz'] or data['quiz'] == "":
    	return JsonResponse({'errors':'Quiz name can not be empty', 'status':'error'})
    if not data['question'] or data['question'] == "":
    	return JsonResponse({'errors':'Question  can not be empty', 'status':'error'})

    quiz = Quiz.objects.filter(id=int(data['quiz'])).first()
    if not quiz:
    	return JsonResponse({'errors':'Selected Quiz was not found', 'status':'error'})

    question_exist = Question.objects.filter(question_text=data['question'], quiz=quiz).first()
    if question_exist:
    	return JsonResponse({'errors':'the question already exists', 'status':'error'})
    question = Question.objects.create(question_text=data['question'], quiz=quiz)
    question.save()
    return JsonResponse({'message': 'question added successfully', 'status': 'success'}, status=200)

@check_leave
@csrf_protect	
def delete_question(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'question' : 'question_id'
    }

    if not data['question'] or data['question'] != "":
    	return JsonResponse({'errors':'question name can not be empty', 'status':'error'})

    question = Question.objects.filter(id=int(data['question_id'])).first()
    if not question:
    	return JsonResponse({'errors':'Selected Question does not exist', 'status':'error'})
    question.delete()
    
    return JsonResponse({'message': 'question added successfully', 'status': 'success'}, status=200)


@check_leave
@csrf_protect	
def add_answer(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'answer' : json_data.get('answer'),
    	'question' : json_data.get('question_id'),
    	'is_correct': json_data.get('is_correct')
    }

    if not data['answer'] or data['answer'] == "":
    	return JsonResponse({'errors':'Answer name can not be empty', 'status':'error'})
    if not data['question'] or data['question'] == "":
    	return JsonResponse({'errors':'Question  can not be empty', 'status':'error'})
    if not data['is_correct'] or data['is_correct'] == "":
    	return JsonResponse({'errors':'Question  can not be empty', 'status':'error'})    	
    
    question = Question.objects.filter(id=int(data['question'])).first()
    if not question:
    	return JsonResponse({'errors':'Selected Question was not found', 'status':'error'})

    if data['is_correct'] == "true":
    	answer = Answer.objects.create(answer_text=data['answer'], question=question,is_correct=True )
    elif data['is_correct'] == "false":
    	answer = Answer.objects.create(answer_text=data['answer'], question=question,is_correct=False )
    else:
    	return JsonResponse({'errors':'Error adding answer', 'status':'error'})
    answer.save()
    return JsonResponse({'message': 'question added successfully', 'status': 'success'}, status=200)

@check_leave
@csrf_protect	
def delete_answer(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'answer' : json_data.get('answer_id')
    }
    print(data)
    if not data['answer'] or data['answer'] == "":
    	return JsonResponse({'errors':'answer name can not be empty', 'status':'error'})

    answer = Answer.objects.filter(id=int(data['answer'])).first()
    if not answer:
    	return JsonResponse({'errors':'Selected answer does not exist', 'status':'error'})
    answer.delete()
    return JsonResponse({'message': 'answer added successfully', 'status': 'success'}, status=200)

@check_leave
@csrf_protect	
def enable_or_disable_quiz(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    data = {
    	'status' : json_data.get('status'),
    	'quiz' : json_data.get('quiz_id')
    }
    print(data)
    if not data['status'] or data['status'] == "":
    	return JsonResponse({'errors':'status name can not be empty', 'status':'error'})
    if not data['quiz'] or data['quiz'] == "":
    	return JsonResponse({'errors':'quiz name can not be empty', 'status':'error'})

    quiz = Quiz.objects.filter(id=int(data['quiz'])).first()
    if not quiz:
    	return JsonResponse({'errors':'Selected status does not exist', 'status':'error'})
    if data['status'] == "enable":
    	quiz.is_active = True
    	quiz.save()
    elif data['status'] == "disable":
    	quiz.is_active = False
    	quiz.save()
    else:
    	return JsonResponse({'errors': { "Quiz" : ['Error updating quiz ']}, 'status':'error'}, status=403)

    return JsonResponse({'message': 'quiz status is updated Successfully', 'status': 'success'}, status=200)


@csrf_protect
def take_quiz(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    # data ={
	# 	    'quiz_id':json_data.get('quiz_id'),
	# 	   	'quiz_data':{
	# 	   				'question_id':json_data.get('question_id'),
	# 				    'answer_id' : json_data.get("answer_id")
	# 	   			}
	# 	   } 
    print("--------------------------------")
    print(json_data)
    
    print("--------------------------------")
    score = 0
    total = len(json_data) - 2
   
    quiz = json_data.get('quiz')
    quiz = Quiz.objects.filter(id=int(quiz)).first()
    for key, value in json_data.items():
    	if value != "" and key != "quiz":
    		try:
    			question = Question.objects.filter(id=int(key)).first()
    		except ValueError:
    			pass
    		answer = Answer.objects.filter(id=int(value)).first()
    		quiz_answers = QuizAnswers.objects.create(user=request.user, quiz=quiz, question=question, answer=answer)
    		quiz_answers.save()
    		if answer:
    			if answer.is_correct:
    				score +=1
    total_score = (score/total) * 100

    
    if quiz:
    	if total_score >= 60.0 :
    		quiz_results = QuizResults.objects.create(user=request.user, quiz=quiz,results="passed", total=total_score )
    		
    	else:
    		quiz_results = QuizResults.objects.create(user=request.user, quiz=quiz,results="failed", total=total_score)
      
      	
    quiz_results.save()
    return redirect('job_application', jobID=int(json_data.get('jobID')))
    # return JsonResponse({'message': 'quiz Submitedd Successfully', 'status': 'success'}, status=200)

@csrf_protect 
def score_add_question(request):
   
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

    scoreboard_id = json_data.get('scoreboard_id')
    scoreboard = get_object_or_404(Scoreboard, id=int(scoreboard_id))
    question_text = json_data.get("question_text")
    if question_text:
        question = ScoreQuestion.objects.create(scoreboard=scoreboard, text=question_text)
        question.save()
        return JsonResponse({'message': 'Added Question/Objective  successfully', 'status': 'success'}, status=200)
    return JsonResponse({'errors': { "Error" : ['Something went wrong ']}, 'status':'error'}, status=403)

@csrf_protect
def score_delete_question(request):
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    question_id = json_data.get('question_id')
    question = get_object_or_404(ScoreQuestion, id=int(question_id))
    scoreboard_id = question.scoreboard.id
    question.delete()
    return JsonResponse({'message': 'Delete Question/Objective  successfully', 'status': 'success'}, status=200)

@csrf_protect
def submit_scoreboard(request, scoreboard_id,application_id):
	if not request.method == 'POST':
		return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
	try:
		json_data = json.loads(request.body)
	except Exception :
		return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

	scoreboard = Scoreboard.objects.filter(id=scoreboard_id).first()
	application = JobApplication.objects.filter(id=int(application_id)).first()
	if not application:
		return JsonResponse({'errors': { "Error" : ['application not found']}, 'status':'error'}, status=403)

	if scoreboard:
		for question in scoreboard.questions.all():
			score_key = f"score_{question.id}"
			score_value = json_data.get(score_key)
			
			results = ScoreResult.objects.create(scoreboard=scoreboard,application=application,question=question,score=int(score_value))
			results.save()
		 
		application.status = "short_list"
		application.previous_stage = application.current_stage
		application.current_stage = "short listing stage"
		application.staff = request.user
		application.is_rejected = False 
		application.filterd_out = True 
		application.reason = ""
		application.save()
		feed_back = FeedBack.objects.create(user=application.user,job=application.job,message="moved to Short-List stage",status="Short-List")
		feed_back.save()
		return JsonResponse({'message': 'Saving Scorecard results', 'status': 'success'}, status=200)
	else:
		return JsonResponse({'errors': { "Error" : ['Scorecard not found ']}, 'status':'error'}, status=403)

