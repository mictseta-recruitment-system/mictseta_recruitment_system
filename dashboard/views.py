from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.contrib.auth.models import User
from jobs.models import JobPost
from datetime import datetime
from django.http import HttpResponse
# Create your views here.


@ensure_csrf_cookie
def panel(request):
	if request.user.is_authenticated:

		return render(request,'panel.html')
	else:
		return redirect('render_auth_page')

@csrf_protect
def view_users(request):
	if request.user.is_authenticated:
		users = User.objects.all()

		return render(request,'view_users.html',{'users':users})
	else:
		return redirect('render_auth_page')

@csrf_protect
def add_job(request):
	if request.user.is_authenticated:
		return render(request,'add_job.html')
	else:
		return redirect('render_auth_page')

@csrf_protect
def update_job(request):
	if request.user.is_authenticated:
		return render(request,'update_job.html')
	else:
		return redirect('render_auth_page')

@csrf_protect
def view_jobs(request):
	if request.user.is_authenticated:
		jobs = JobPost.objects.all()
		return render(request,'view_job.html',{'jobs':jobs})
	else:
		return redirect('authenticate.render_auth_page')

@csrf_protect
def job_details(request, jobID):
	if request.user.is_authenticated:
		try:
			job = JobPost.objects.get(id=int(jobID))
			
			return render(request,'detailed_job.html',{'job':job})
		except Exception as e:
			return HttpResponse(f"<h1> Sever Error : Job not Found : {e}</h1>")
	else:
		return redirect('authenticate.render_auth_page')