from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
from django.contrib.auth.models import User
from jobs.models import JobPost, Notification
from profiles.models import Leave, Attendance, Shift
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from datetime import datetime
import datetime as dates
from .models import Backup


@ensure_csrf_cookie
def panel(request):
	if request.user.is_authenticated:

		return render(request,'panel.html')
	else:
		return redirect('render_auth_page')

@ensure_csrf_cookie
def emp_panel(request):
	if request.user.is_authenticated:
		shift_start_time = request.user.shift.start_time
		shift_end_time = request.user.shift.end_time
		current_time =  datetime.now()
		
		att = Attendance.objects.filter(employee=request.user, date=dates.date.today()).exists()
		if att :
			att = Attendance.objects.get(employee=request.user, date=dates.date.today())
			status = att.active
		else:
			status = "Inactive"

		if current_time.month  < 10 :

			start_time = f"{current_time.year}-0{current_time.month}-{current_time.day}T{shift_start_time}" 
			end_time = f"{current_time.year}-0{current_time.month}-{current_time.day}T{shift_end_time}"
		else:
			start_time = f"{current_time.year}-{current_time.month}-{current_time.day}T{shift_start_time}" 
			end_time = f"{current_time.year}-{current_time.month}-{current_time.day}T{shift_end_time}"

		return render(request,'emp_panel.html', {'start_time':start_time,'end_time':end_time,'status':status})
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
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
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
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		jobs = JobPost.objects.all()
		all_jobs = len(jobs)
		open_jobs= len(JobPost.objects.filter(status="Approved"))
		pending_jobs = len(JobPost.objects.filter(status="waiting"))
		pending_jobs = len(JobPost.objects.filter(status="pending")) + pending_jobs
		closed_jobs = len(JobPost.objects.filter(status="closed"))
		return render(request,'view_job.html',{'jobs':jobs, 'all_jobs':all_jobs,'open_jobs':open_jobs, 'pending_jobs':pending_jobs,'closed_jobs':closed_jobs})
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
		current_time = now()
		for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
			if leave.start_date <= current_time <= leave.end_date:
				return HttpResponse("<h1>Request denied: you are on leave</h1>")
		if request.user.is_superuser:
			return render(request,'add_staff.html')
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
		return render(request,'update_staff.html', {'staff':staff})
	else:
		return redirect('render_auth_page')


def employee_details(request, empID):
	if request.user.is_authenticated:
		
		emp = User.objects.get(id=empID)
		if request.user.is_superuser or request.user.id == emp.id:
			return render(request, 'employee_details.html',{'emp':emp})
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
			return render(request, 'manage_leave.html', {'emps':emps})
		else:
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')

def view_leave(request):
    if request.user.is_authenticated:
        if request.user.is_staff:

            try:
                leaves = Leave.objects.all()
                
                return render(request, 'view_leave.html', {'leaves':leaves})

            except Exception as e:
                return HttpResponse(f'view leave: {e}')
        else:       
            return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
    else:
       return redirect('render_auth_page')

def manage_attendance(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			try:
				attendances = Attendance.objects.all()
				return render(request,'attendance.html',{'attendances':attendances})
			except Exception as e:
				return HttpResponse(f'view Attendance: {e}')
		else:       
			return HttpResponse(f"<h1> Sever Error : Permission Denied </h1>")
	else:
		return redirect('render_auth_page')





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




from .db_backups import my_backup
def backup_database(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			backups = Backup.objects.all()
			return render(request, 'backup.html', {'backups':backups} )
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
