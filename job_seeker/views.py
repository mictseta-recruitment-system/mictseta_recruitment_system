from django.shortcuts import render
from jobs.models import JobPost
# Create your views here.
def job_seeker_dashboard(request):
    return render(request, 'job_seeker_dashboard.html')

def personal_details(request):
    return render(request, 'personal_details.html')

def academic_qualifications(request):
    return render(request, 'academic_qualifications.html')

def language_proficiency(request):
    return render(request, 'language_proficiency.html')

def soft_skills(request):
    return render(request, 'soft_skills.html')

def computer_skills(request):
    return render(request, 'computer_skills.html')

def working_experience(request):
    return render(request, 'working_experience.html')

def referees(request):
    return render(request, 'referees.html')

def supporting_documents(request):
    return render(request, 'supporting_documents.html')

def job_details(request):
    job_list = JobPost.objects.filter(status='open')
    return render(request, 'jobseeker_job_details.html', {'job_list':job_list})

def application_tracking(request):
    return render(request, 'application_tracking.html')

def interviews(request):
    return render(request, 'interviews.html')

def job_information(request):
    return render(request, 'job_information.html')

def feedback(request):
    return render(request, 'feedback.html')

def logout(request):
    return render(request, 'logout.html')



