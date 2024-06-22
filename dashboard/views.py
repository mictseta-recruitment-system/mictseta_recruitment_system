from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.contrib.auth.models import User
from jobs.models import JobPost, Notification
from datetime import datetime
from django.http import HttpResponse


@ensure_csrf_cookie
def panel(request):
	if request.user.is_authenticated:

		return render(request,'panel.html')
	else:
		return redirect('render_auth_page')

@csrf_protect
def view_staff(request):
	if request.user.is_authenticated:
		staff = User.objects.filter(is_staff=True)

		return render(request,'view_staff.html',{'staffs':staff})
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
		
		if request.user.is_superuser:
			return render(request,'add_staff.html')
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')
	
@csrf_protect
def update_staff(request, staffID):
	if request.user.is_authenticated:
		staff = User.objects.get(id=int(staffID))
		return render(request,'update_staff.html', {'staff':staff})
	else:
		return redirect('render_auth_page')



def employee_details(request, empID):
	if request.user.is_authenticated:
		
		if request.user.is_superuser:
			emp = User.objects.get(id=empID)
			return render(request, 'employee_details.html',{'emp':emp})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')