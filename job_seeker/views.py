from django.shortcuts import render

# Create your views here.
def job_seeker_dashboard(request):
	return render(request, 'job_seeker_dashboard.html')