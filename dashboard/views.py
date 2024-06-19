from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.contrib.auth.models import User
from jobs.models import JobPost, Notification
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
		return redirect('render_auth_page')

@csrf_protect
def job_details(request, jobID):
	if request.user.is_authenticated:
		try:
			job = JobPost.objects.get(id=int(jobID))
			
			return render(request,'detailed_job.html',{'job':job})
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
				return render(request,'notification.html',{'notifications':notification.reverse()})
			elif request.user.is_staff:
				notification = Notification.objects.filter(user=request.user)
			return render(request,'notification.html',{'notifications':notification.reverse()})
		except Exception as e:
			return HttpResponse(f"<h1> Sever Error : Job not Found : {e}</h1>")
	else:
		return redirect('render_auth_page')


def add_staff_page(request):
	if request.user.is_authenticated:
		try:
			if request.user.is_superuser:
				return render(request,'add_staff.html')
			else:
				return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
				
		except Exception as e:
			return HttpResponse(f"<h1> Sever Error : Job not Found : {e}</h1>")
	else:
		return redirect('render_auth_page')
	