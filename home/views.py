from django.shortcuts import render
from jobs.models import JobPost
# Create your views here.
def about_us(request):
    
    return render(request, "about_us.html")

def contact_us(request):
    return render(request, "contact_us.html")

def home(request):
    jobs = JobPost.objects.filter(is_approved=True)

    return render(request,'index.html', {'jobs':jobs})


def job_details(request):
    jobs = JobPost.objects.filter(is_approved=True)
    return render(request,'job_details.html')