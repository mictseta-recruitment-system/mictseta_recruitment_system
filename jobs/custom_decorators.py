from django.utils.timezone import now
from .models import  JobApplication, Interview

def change_application_status(function=None):
	def decorator(view_func):
		def _wrapper(request, *args, **kwargs):
			applications = JobApplication.objects.all()
			interviews = Interview.objects.all()
			for application in applications:
				if application.job.status=="closed":
					application.status = 'rejected'
					application.reason = "system closed the job - Expired"
					application.save()
					cleened = [interview.delete() for interview in interviews if interview.application == application]
			return view_func(request,*args,**kwargs)

		return _wrapper
	if function:
		return decorator(function)

def check_leave(function=None):
	def decorator(view_func):
		def _wrapper(request,*args, **kwargs):
			current_time = now()
			for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
				if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
					return HttpResponse("<h1>Request denied: you are on leave</h1>")
			return view_func(request, *args,**kwargs)
		return _wrapper
	if function:
		return decorator(function)
			