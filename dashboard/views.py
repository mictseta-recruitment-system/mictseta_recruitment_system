from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.contrib.auth.models import User
from jobs.models import JobPost, Notification, JobApplication,Interview,QuizResults,Quiz,Question,Answer,FeedBack, QuizAnswers, Alert,Scoreboard, ScoreQuestion,ScoreResult
from profiles.models import Leave, Attendance, Shift
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from datetime import datetime
import datetime as dates
from .models import Backup
from task_manager.models import Category, Task
import json
from django.db.models import Q
from easyaudit.models import CRUDEvent, LoginEvent
from jobs.custom_decorators import check_leave, change_application_status
from config.models import JobTitle, Industry
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle

@ensure_csrf_cookie
def panel(request):
	if request.user.is_authenticated:
		notify_len = len(Notification.objects.all())
		notification = Notification.objects.all()
		if request.user.is_superuser:
			categoreis = Category.objects.filter(user=request.user).distinct()
		else:
			categoreis = Category.objects.filter(task__assigned_to=request.user).distinct()
		cats = []
		data = []
		for cat in categoreis:
			cats.append(cat.name)
			data.append(len(Task.objects.filter(category=cat, is_complete=False)))
		return render(request,'panel.html', { 'notify_len':notify_len, 'notifications':notification,'cats':json.dumps(cats), 'datas':json.dumps(data)})
	else:
		return redirect('render_auth_page')

@ensure_csrf_cookie
def emp_panel(request):
	if request.user.is_authenticated:
		#### Shift Code #####
		# shift_start_time = request.user.shift.start_time
		# shift_end_time = request.user.shift.end_time
		# current_time =  datetime.now()
		
		# att = Attendance.objects.filter(employee=request.user, date=dates.date.today()).exists()
		# if att :
		# 	att = Attendance.objects.get(employee=request.user, date=dates.date.today())
		# 	status = att.active
		# else:
		# 	status = "Inactive"

		# if current_time.month  < 10 :

		# 	start_time = f"{current_time.year}-0{current_time.month}-{current_time.day}T{shift_start_time}" 
		# 	end_time = f"{current_time.year}-0{current_time.month}-{current_time.day}T{shift_end_time}"
		# elif current_time.day < 10 :
		# 	start_time = f"{current_time.year}-0{current_time.month}-{current_time.day}T{shift_start_time}" 
		# 	end_time = f"{current_time.year}-0{current_time.month}-{current_time.day}T{shift_end_time}"
		# else:
		# 	start_time = f"{current_time.year}-{current_time.month}-{current_time.day}T{shift_start_time}" 
		# 	end_time = f"{current_time.year}-{current_time.month}-{current_time.day}T{shift_end_time}"
		
		if request.user.is_superuser:
			notification = Notification.objects.all()
			notify_len = len(Notification.objects.filter(is_seen=False))
		else:
			notification = Notification.objects.filter(user=request.user)
			notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))

		if request.user.is_superuser:
			categoreis = Category.objects.filter(Q(user=request.user) | Q(task__assigned_to=request.user)).distinct()
		else:
			categoreis = Category.objects.filter(task__assigned_to=request.user).distinct()
			
		cats = []
		data = []
		for cat in categoreis:
			cats.append(cat.name)
			data.append(len(Task.objects.filter(category=cat, is_complete=False, assigned_to=request.user)))
		alerts = None
		if request.user.staffprofile.department == "FINANCE":
			alerts = Alert.objects.filter(step=2).all()
		if request.user.staffprofile.department == "CEO":
			alerts = Alert.objects.filter(step=2, completed=True)
		if request.user.staffprofile.department == "HR":
			alerts = Alert.objects.filter(Q(step=3, status="pending") | Q(step=5))
		if request.user.staffprofile.department == "LINE":
			alerts = Alert.objects.filter(Q(step=3, status="approved") | Q(step=4))

		alerts = alerts.order_by('-id')
		return render(request,'emp_panel.html', {'notifications':notification.reverse(), 'notify_len':notify_len, 'cats':json.dumps(cats), 'datas':json.dumps(data), 'alerts':alerts})
	else:
		return redirect('render_auth_page')

@csrf_protect
def view_staff(request):
	if request.user.is_authenticated:
		staff = User.objects.filter(is_staff=True)
		staff = staff.order_by('-id')
		if request.user.is_superuser:
			notify_len = len(Notification.objects.filter(is_seen=False))
			notify_len = notify_len.order_by('-id')
		else:
			notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			notify_len = notify_len.order_by('-id')
		return render(request,'view_staff.html',{'staffs':staff,'notify_len':notify_len})
	else:
		return redirect('render_auth_page')


@csrf_protect
def quiz_results(request,quiz_id, user_id, application_id):
	if request.user.is_authenticated:


		quiz_result = QuizAnswers.objects.filter(user=user_id, quiz=quiz_id).all()
		answers = Answer.objects.all()
		user = User.objects.filter(id=int(user_id)).first()
		application = JobApplication.objects.filter(id=int(application_id)).first()
		notify_len = notify_len.order_by('-id')

		return render(request, 'quiz_results.html', {'results':quiz_result, 'application':application, 'seeker':user, 'answers':answers})
	else:
		return redirect('render_auth_page')



@csrf_protect
def job_applications(request):
	if request.user.is_authenticated:
		applications = JobApplication.objects.all()
		applied_jobs = JobPost.objects.filter(jobapplication__isnull=False).distinct()
		interview = Interview.objects.all()
		applications = applications.order_by('-id')
		interview = interview.order_by('-id')
		
		return render(request, 'job_applications.html', {'applications':applications,'interviews':interview, 'applied_jobs':applied_jobs})
	else:
		return redirect('render_auth_page')


@csrf_protect
def calender(request):
	if request.user.is_authenticated:
		interviews = Interview.objects.all()
		interview_list = []
		for interview in interviews:
			add_to_list = {

						'groupID':'999',
						'id':f'{interview.id}',
        				'title': f'{interview.user.email}',
        				'start': f'{interview.date}T{interview.start_time}',
        				'end': f'{interview.date}T{interview.end_time}'
     		}
			interview_list.append(add_to_list)

		interview_list_json = json.dumps(interview_list)
		return render(request, 'calender.html',{'interviews':interview_list_json})
	else:
		return redirect('render_auth_page')

@csrf_protect
def filter_job_application(request,jobID):
	if request.user.is_authenticated:
		job_applications = JobApplication.objects.filter(job__id=jobID)
		cnt=0
		interview = Interview.objects.filter(application__job__id=jobID)
		data = []

		for application in job_applications:
			total_score = 0
			total_questions = 0 
			points = 0
			results = ScoreResult.objects.filter(application=application).all()
			if results:
				for result in results:
					total_score += int(result.score)
					total_questions += 1

				to_add = {
					'application':application,
					'points' : round((total_score/(total_questions*4) ) *100,2)
				}
				data.append(to_add)
		return render(request,'job_applications.html',{'applications':job_applications,'interviews':interview, 'cnt':cnt,'filtered':True, 'results':data})
	else:
		return redirect('render_auth_page')

@csrf_protect
def application_jobs(request):
	if request.user.is_authenticated:
		applied_jobs = JobPost.objects.all()
		vac_list = []

		for vacancy in applied_jobs:
			appl = vacancy.jobapplication_set.all()
    
			data = {
		        'vacancy': vacancy,
		        'applications': appl.count(),
		        'filtered': vacancy.jobapplication_set.filter(status="pending").count(),  # Corrected the typo here
		        'shortlist': vacancy.jobapplication_set.filter(status="short_list").count(),
		        'interview': vacancy.jobapplication_set.filter(status="interview").count(),
		        'selected': vacancy.jobapplication_set.filter(status="selected").count(),
		        'rejected': vacancy.jobapplication_set.filter(status="rejected").count(),
		        'onboard': vacancy.jobapplication_set.filter(status="approved").count()
		    }
    
			vac_list.append(data)
		vac_list.reverse()
		return render(request,'application_jobs.html',{'vac_list':vac_list})
	else:
		return redirect('render_auth_page')

@csrf_protect
def add_job(request):
	if request.user.is_authenticated:
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		if request.user.is_superuser:
			notify_len = len(Notification.objects.filter(is_seen=False))
		else:
			notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
		employees = User.objects.filter(is_staff=True)
		if request.user.is_superuser:
			employees = User.objects.filter(is_staff=True)
		else:
			employees = User.objects.filter(id=request.user.id)
		job_title = JobTitle.objects.all()
		industry = Industry.objects.all()
		return render(request,'add_job.html',{'notify_len':notify_len,'employees':employees, 'job_titles':job_title, 'industries':industry})
	else:
		return redirect('render_auth_page')

@csrf_protect
def update_job(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			notify_len = len(Notification.objects.filter(is_seen=False))
		else:
			notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))

		return render(request,'update_job.html',{'notify_len':notify_len})
	else:
		return redirect('render_auth_page')


@csrf_protect
def view_jobs(request):
	if request.user.is_authenticated:
		current_time = now()
		# for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
		# 	if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
		# 		return HttpResponse("<h1>Request denied: you are on leave</h1>")
		jobs = JobPost.objects.all()
		for job in jobs:
			if job.status != "closed":
				if current_time > job.end_date :
					job.status = "expired"
					job.save()

		all_jobs = len(jobs)
		open_jobs= len(JobPost.objects.filter(status="open"))
		pending_jobs = len(JobPost.objects.filter(Q(status="waiting") | Q(status="pending")))
		closed_jobs = len(JobPost.objects.filter(Q(status="closed") | Q(status="expired")))

		if request.user.is_superuser:
			notify_len = len(Notification.objects.filter(is_seen=False))
			
		else:
			notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
		jobs = jobs.order_by('-id')
		return render(request,'view_job.html',
			{	
			'jobs':jobs, 
			'all_jobs':all_jobs,
			'open_jobs':open_jobs, 
			'pending_jobs':pending_jobs,
			'closed_jobs':closed_jobs, 
			'notify_len':notify_len,
			},
			status=200)
	else:
		return redirect('render_auth_page')


@csrf_protect
def edit_job(request, jobID):
	if request.user.is_authenticated:
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		try:
			job = JobPost.objects.get(id=int(jobID))
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))

			job_title = JobTitle.objects.all()
			industry = Industry.objects.all()

			languages = LanguageList.objects.all()
			readings = ReadingProficiencyList.objects.all()
			speakings = SpeakingProficiencyList.objects.all()
			writings = WritingProficiencyList.objects.all()
			computer_skills = ComputerSkillsList.objects.all()
			computer_prof = ComputerProficiency.objects.all()
			soft_skill = SoftSkillsList.objects.all()
			soft_prof = SoftProficiency.objects.all()
			qualification = Qualification.objects.all()
			nqf_level = NQF.objects.all()
			print(job.is_complete, job.current_step)
			return render(request,'edit_job.html',
				{
				'job':job, 
				'notify_len':notify_len,
				'job_titles':job_title, 
				'industries':industry,
				'computer_skills':computer_skills,
				'computer_profs':computer_prof,
				'soft_skills':soft_skill,
				'soft_profs':soft_prof,
				'nqf_levels' : nqf_level,
				'qualifications':qualification,
				'languages' : languages,
				'readings' : readings,
				'writings' : writings,
				'speakings':speakings
			})
		except Exception as e:
			return HttpResponse(f"<h1> Sever Error : Job not Found : {e}</h1>")
	else:
		return redirect('render_auth_page')

@csrf_protect
def job_details(request, jobID):
	if request.user.is_authenticated:
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		try:
			job = JobPost.objects.get(id=int(jobID))
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request,'detailed_job.html',{'job':job, 'notify_len':notify_len})
		except Exception as e:
			return HttpResponse(f"<h1> Sever Error : Job not Found : {e}</h1>")
	else:
		return redirect('render_auth_page')

@csrf_protect
def get_notifications(request):
	if request.user.is_authenticated:
		try:
			if request.user.is_superuser:
				notification = Notification.objects.all()
				if request.user.is_superuser:
					notify_len = len(Notification.objects.filter(is_seen=False))
				else:
					notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
				return render(request,'notification.html',{'notify_len':notify_len,'notifications':notification.reverse()})
			elif request.user.is_staff:
				notification = Notification.objects.filter(user=request.user)

			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request,'notification.html',{'notify_len':notify_len,'notifications':notification.reverse()})
		except Exception as e:
			return HttpResponse(f"<h1> Sever Error : Notification: {e}</h1>")
	else:
		return redirect('render_auth_page')

@csrf_protect
def delete_notifications(request, notID):
	if request.user.is_authenticated:
		try:
			if request.user.is_superuser:
				notification = Notification.objects.get(id=notID)
				notification.delete()
				notifications = Notification.objects.all()
				return render(request,'notification.html',{'notifications':notifications.reverse()})
			elif request.user.is_staff:
				notification = Notification.objects.get(id=notID)
				notification.delete()
				notifications = Notification.objects.filter(user=request.user)
			return render(request,'notification.html',{'notifications':notifications.reverse()})
		except Exception as e:
			return HttpResponse(f"<h1> Delete notification : Job not Found : {e}</h1>")
	else:
		return redirect('render_auth_page')

def add_staff_page(request):
	if request.user.is_authenticated:
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date:
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		if request.user.is_superuser:
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request,'add_staff.html', {'notify_len':notify_len})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')
	
@csrf_protect
def update_staff(request, staffID):
	if request.user.is_authenticated:
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date:
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		staff = User.objects.get(id=int(staffID))
		if request.user.is_superuser:
			notify_len = len(Notification.objects.filter(is_seen=False))
		else:
			notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
		return render(request,'update_staff.html', {'staff':staff, 'notify_len':notify_len})
	else:
		return redirect('render_auth_page')

def jobsekeer_details(request, seekerID,jobID):
	if request.user.is_authenticated:
		
		seeker = User.objects.get(profile__uuid=seekerID)
		if request.user.is_staff:
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			application = JobApplication.objects.filter(user=seeker,job__id=int(jobID)).first()
			feedback = FeedBack.objects.filter(user=seeker,job=application.job)
			quiz_id = Quiz.objects.filter(job=application.job).first()
			print(quiz_id, "---", quiz_id.id)
			if quiz_id:
				quiz = QuizResults.objects.filter(user=seeker, quiz=quiz_id.id).first()
				print(quiz)
			else:
				quiz = {}
			vacancy = JobPost.objects.get(id=int(jobID))
			scoreboard = Scoreboard.objects.filter(vacancy=vacancy).first()
			res = scoreboard.scoreresult_set.filter(application=application)
			if res:
				return render(request, 'job_seeker_details.html',{'seeker':seeker,'notify_len':notify_len,'application':application,'feedbacks':feedback,'quiz':quiz,'score':True, "scoreboard":scoreboard, 'scored':True})

			return render(request, 'job_seeker_details.html',{'seeker':seeker,'notify_len':notify_len,'application':application,'feedbacks':feedback,'quiz':quiz,'scoreboard':scoreboard})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

def jobsekeer_details_score(request, seekerID,jobID):
	if request.user.is_authenticated:
		
		seeker = User.objects.get(profile__uuid=seekerID)
		if request.user.is_staff:
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			application = JobApplication.objects.filter(user=seeker,job__id=int(jobID)).first()
			feedback = FeedBack.objects.filter(user=seeker,job=application.job)
			quiz_id = Quiz.objects.filter(job=application.job).first()
			print(quiz_id, "---", quiz_id.id)
			if quiz_id:
				quiz = QuizResults.objects.filter(user=seeker, quiz=quiz_id.id).first()
				print(quiz)
			else:
				quiz = {}
			vacancy = JobPost.objects.get(id=int(jobID))
			scoreboard = Scoreboard.objects.filter(vacancy=vacancy).first()
			res = scoreboard.scoreresult_set.filter(application=application)
			if res:
				return render(request, 'job_seeker_details.html',{'seeker':seeker,'notify_len':notify_len,'application':application,'feedbacks':feedback,'quiz':quiz,'score':True, "scoreboard":scoreboard, 'scored':True})


			return render(request, 'job_seeker_details.html',{'seeker':seeker,'notify_len':notify_len,'application':application,'feedbacks':feedback,'quiz':quiz,'score':True, "scoreboard":scoreboard})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

def employee_details(request, empID):
	if request.user.is_authenticated:
		
		emp = User.objects.get(id=empID)
		if request.user.is_superuser or request.user.id == emp.id:
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request, 'employee_details.html',{'emp':emp,'notify_len':notify_len})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

def manage_leave(request):
	if request.user.is_authenticated:

		if request.user.is_staff:
			#emps = User.objects.filter(is_staff=True)
			from django.db.models import Count

			# Filter staff users who have one or more leaves
			emps = User.objects.filter(is_staff=True).annotate(leave_count=Count('leave')).filter(leave_count__gt=0)
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request, 'manage_leave.html', {'emps':emps,'notify_len':notify_len})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

def view_leave(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			try:
				leaves = Leave.objects.all()
				if request.user.is_superuser:
					notify_len = len(Notification.objects.filter(is_seen=False))
				else:
					notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
				return render(request, 'view_leave.html', {'leaves':leaves,'notify_len':notify_len})
			except Exception as e:
				return HttpResponse(f'view leave: {e}')
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')
		
#### Shift Code #####
# def manage_attendance(request):
# 	if request.user.is_authenticated:
# 		if request.user.is_staff:
# 			try:
# 				attendances = Attendance.objects.all()
# 				if request.user.is_superuser:
# 					notify_len = len(Notification.objects.filter(is_seen=False))
# 				else:
# 					notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
# 				return render(request,'attendance.html',{'attendances':attendances,'notify_len':notify_len})
# 			except Exception as e:
# 				return HttpResponse(f'view Attendance: {e}')
# 		else:       
# 			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
# 	else:
# 		return redirect('render_auth_page')





from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
def fetch_resources(uri, rel):
    from django.conf import settings
    import os.path
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def attendance_generate_pdf_report(request):
    shifts = Shift.objects.all()
    attendances = Attendance.objects.all()
    context = {
        'shifts': shifts,
        'attendances': attendances,
    }
    pdf = render_to_pdf('pdf_attendance_template.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def leave_generate_pdf_report(request):
    shifts = Shift.objects.all()
    leaves = Leave.objects.all()
    context = {
        'leaves': leaves,
    }
    pdf = render_to_pdf('pdf_leave_templates.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def task_manager(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			if request.user.is_superuser:
				categoreis = Category.objects.filter(Q(user=request.user) | Q(task__assigned_to=request.user)).distinct()
			else:
				categoreis = Category.objects.filter(Q(user=request.user) | Q(task__assigned_to=request.user)).distinct()
			# tasks = Task.objects.filter()
			if request.user.is_superuser:
				assignees = User.objects.filter(is_staff=True)
			else:
				assignees = User.objects.filter(id=request.user.id)
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request, 'task_manager.html',{ 'categories':categoreis, 'assignees':assignees,'notify_len':notify_len})
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

from .db_backups import my_backup
def backup_database(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			backups = Backup.objects.all()
			if request.user.is_superuser:
				notify_len = len(Notification.objects.filter(is_seen=False))
			else:
				notify_len = len(Notification.objects.filter(user=request.user,is_seen=False))
			return render(request, 'backup.html', {'backups':backups, 'notify_len':notify_len} )
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')


def backup_db(request):
	from django.utils import timezone
	if request.user.is_authenticated:
	  	if request.method == 'GET':
	  		try:
		  		time = datetime.now().strftime('%H:%M:%S')
		  		current_date = datetime.now().strftime('%H_%M_%S-%d_%m_%Y')
		  		date = timezone.now().date()
		  		filename = f'Backup-{current_date}.backup'
		  		backup_db = Backup(user=request.user, filename=filename, date=date, time=time)
		  		backup_db.save()
		  		my_backup(filename)
		  	except Exception as e:
		  		return JsonResponse({'errors': f'{e}', 'status':'error'}, status=400)
	  		return JsonResponse({'message': 'Database Backup success' , 'status':'success'})
	  	else:
	  		return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
	else:
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)

def delete_db(request,dbID):
	import os
	from pathlib import Path
	BASE_DIR = Path(__file__).resolve().parent.parent
	if request.user.is_authenticated:
	  	if request.method == 'GET':
	  		try:
		  		db_entry = Backup.objects.filter(id=int(dbID)).exists()
		  		if db_entry:
		  			db_entry = Backup.objects.get(id=int(dbID))
		  			# file_path = '/'.join(['backup','database',str(db_entry.filename)])
		  			file_to_delete = str(BASE_DIR / 'backup' / 'database' / db_entry.filename)
		  			if os.path.isfile(file_to_delete):
		  				os.remove(file_to_delete)
		  			db_entry.delete()
	  				return JsonResponse({'message': 'Database Backup Deleted' , 'status':'warning'})
		  	except Exception as e:
		  		return JsonResponse({'errors':{'server error' : [f'{e}']}, 'status':'error'}, status=400)
	  	else:
	  		return JsonResponse({'errors':{ 'MEthod':['Forbidden 403']}, 'status':'error'}, status=400)
	else:
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)

from .db_backups import my_restore
def restore_db(request, dbID):
	from django.utils import timezone
	if request.user.is_authenticated:
	  	if request.method == 'GET':
	  		try:
		  		
		  		restore_db = Backup.objects.get(id=int(dbID))
		  		
	  			return JsonResponse({'message': f'Database restored to {restore_db.filename}' , 'status':'success'})
		  		my_restore(restore_db.filename)
		  	except Exception as e:
		  		return JsonResponse({'errors': f'{e}', 'status':'error'}, status=400)
	  	else:
	  		return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
	else:
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


def get_log_user_by_id(event):
	try : 
		user =  User.objects.get(id=event.user_id)
		return user 
	except :
		user = "ANONYMOUS"
	return user


def get_changed_fields(event):
	if event != 'null' and event != None: 
		dictionary = json.loads(event)
		return dictionary
	else:
		return event

# Convert the JSON string to a Python dictionary

def crud_events(request):
	if request.user.is_authenticated:
		if request.user.is_superuser :
			cruds = CRUDEvent.objects.all()
			method_type = ('CREATE','UPDATE','DELETE')
			data = []

			for event in cruds:
				event_data = {
					'object_json' 	:get_changed_fields(event.object_json_repr)[0],
					'id'		: event.id,
					'user' 			: get_log_user_by_id(event),
					'event_type' 	: method_type[event.event_type -1],
					'content_type'	: event.content_type.model,
					'object'		: event.object_repr,
					'changed_fields': get_changed_fields(event.changed_fields),
					'date'			: event.datetime,
				}
				data.append(event_data)

			return render(request, 'crud_events.html',{'crud_events':data})
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')







def login_events(request):
	if request.user.is_authenticated:
		if request.user.is_superuser :
			data = []
			login_types = ('LOGIN','LOGOUT','FAILDE LOGIN')
			logins = LoginEvent.objects.all()

			for event in logins :
				event_data = {
					'date'		: event.datetime,
					'method'	: login_types[event.login_type],
					'remote_ip'	: event.remote_ip,
					'user'		: get_log_user_by_id(event),

				}
				data.append(event_data)
			return render(request, 'login_events.html', {'login_events':data})
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')


def login_events_generate_pdf_report(request):
	data = []
	login_types = ('LOGIN','LOGOUT','FAILED LOGIN')
	cruds = LoginEvent.objects.all()

	for event in cruds :
		event_data = {
			'date'		: event.datetime,
			'method'	: login_types[event.login_type],
			'remote_ip'	: event.remote_ip,
			'user'		: get_log_user_by_id(event),
		}
		data.append(event_data)
	context = {
        'login_events': data,
    }
	pdf = render_to_pdf('pdf_login_events.html', context)
	return HttpResponse(pdf, content_type='application/pdf')

def crud_events_generate_pdf_report(request):
	cruds = CRUDEvent.objects.all()
	method_type = ('CREATE','UPDATE','DELETE')
	data = []

	for event in cruds:
		event_data = {
			
			'id'			: event.id,
			'user' 			: get_log_user_by_id(event),
			'event_type' 	: method_type[event.event_type -1],
			'content_type'	: event.content_type.model,
			'object'		: event.object_repr,
			'changed_fields': get_changed_fields(event.changed_fields),
			'date'			: event.datetime,
		}
		
		data.append(event_data)
	
	context = {
        'crud_events': data,
    }

	pdf = render_to_pdf('pdf_crud_events.html', context)
	return HttpResponse(pdf, content_type='application/pdf')


def new_quiz(request, job_id):
	if request.user.is_authenticated:
		if request.user.is_staff:
			job = JobPost.objects.filter(id=int(job_id)).first()
			quiz = Quiz.objects.filter(job__id=int(job_id)).first()
			if not job:
				return render(request, 'new_quiz.html',{})

			return render(request, 'new_quiz.html',{'job':job, 'quiz':quiz})
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

@check_leave
@csrf_protect	
def create_scoreboard(request,job_id):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


    vacancy = JobPost.objects.get(id=int(job_id))
    scoreboard = Scoreboard.objects.filter(vacancy=vacancy).first()
    if not scoreboard:
	    scoreboard = Scoreboard.objects.create(vacancy=vacancy)
	    for education in vacancy.educations.all():
	    	question = f"has qualification in {education.field_of_study}"
	    	score_questions = ScoreQuestion.objects.create(scoreboard=scoreboard, text=question, level="E", max_score=5)
	    	score_questions.save()

	    for experience in vacancy.experiences.all():
	    	question = f"has {experience.duration} in {experience.name}"
	    	score_questions = ScoreQuestion.objects.create(scoreboard=scoreboard, text=question, level="E", max_score=5)
	    	score_questions.save()

	    for skill in vacancy.C_skills.all():
	    	question = f"is {skill.level} in {skill.name}"
	    	score_questions = ScoreQuestion.objects.create(scoreboard=scoreboard, text=question, level="E", max_score=5)
	    	score_questions.save()

	    for skill in vacancy.S_skills.all():
	    	question = f"is {skill.level} in {skill.name}"
	    	score_questions = ScoreQuestion.objects.create(scoreboard=scoreboard, text=question, level="E", max_score=5)
	    	score_questions.save()

	    for requirement in vacancy.requirements.all():
	    	question = requirement.description
	    	score_questions = ScoreQuestion.objects.create(scoreboard=scoreboard, text=question, level="E", max_score=5)
	    	score_questions.save()
	    vacancy.scoreboard = True
	    vacancy.save()
	    scoreboard.save()
	    return render(request, 'create_scoreboard.html',{'scoreboard':scoreboard})

    else:
        return render(request, 'create_scoreboard.html',{'scoreboard':scoreboard})

@check_leave
@csrf_protect	
def view_scoreboard(request,job_id, application_id):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


    vacancy = JobPost.objects.get(id=int(job_id))
    application = JobApplication.objects.get(id=int(application_id))
    scoreboard = Scoreboard.objects.filter(vacancy=vacancy).first()
    results = ScoreResult.objects.filter(scoreboard=scoreboard,application=application).all()
    total_score = 0
    total_questions = 0 
    points = 0
			
    for result in results:
        total_score += int(result.score)
        total_questions += 1

    points = round((total_score/(total_questions*4) ) *100,2)
   
    return render(request, 'view_scoreboard.html',{'scoreboard':scoreboard, 'application':application,'points':points, 'total_score':total_score,'full_score':total_questions*4,'total_questions':total_questions, 'results':results})
