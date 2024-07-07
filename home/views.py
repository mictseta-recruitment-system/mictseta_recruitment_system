from django.shortcuts import render
from jobs.models import JobPost
from django.utils.timezone import now
# Create your views here.
def about_us(request):
    
    return render(request, "about_us.html")

def contact_us(request):
    return render(request, "contact_us.html")

def home(request):
    current_time = now()
    jobs = JobPost.objects.filter(is_approved=True)
    for job in jobs:
        if job.status != "closed":
            if current_time > job.end_date :
                job.status = "closed"
                job.save()
    jobs = JobPost.objects.filter(status="open") 
    print(jobs)
    return render(request,'index.html', {'jobs':jobs})


def job_details(request):
    jobs = JobPost.objects.filter(is_approved=True)
    for job in jobs:
            if current_time > job.end_date :
                job.status = "closed"
                job.save()
    return render(request,'job_details.html')