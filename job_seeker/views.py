from django.shortcuts import render
from jobs.models import JobPost, SkillList, LanguageList
from profiles.models import SupportingDocuments
# Create your views here.
def job_seeker_dashboard(request):
    return render(request, 'job_seeker_dashboard.html')

def personal_details(request):
    return render(request, 'personal_details.html')
def address_details(request):
    return render(request, 'address_details.html')

def academic_qualifications(request):
    return render(request, 'academic_qualifications.html')

def language_proficiency(request):
    languages = LanguageList.objects.all()  
    return render(request, 'language_proficiency.html', {'languages': languages})

def soft_skills(request):
    soft_skills = SkillList.objects.filter(skill_type="Soft skills")

    return render(request, 'soft_skills.html', {'soft_skills':soft_skills})

def computer_skills(request):
    computer_skills = SkillList.objects.filter(skill_type="Computer skills")
    
    return render(request, 'computer_skills.html', {'computer_skills': computer_skills})

def working_experience(request):
    return render(request, 'working_experience.html')

def referees(request):
    return render(request, 'referees.html')

def supporting_documents(request):
    docs = SupportingDocuments.objects.filter(user=request.user)
    return render(request, 'supporting_documents.html',{"docs":docs})

def job_details(request):
    job_list = JobPost.objects.filter(status='open')
    return render(request, 'jobseeker_job_details.html', {'job_list':job_list})

def application_tracking(request):
    return render(request, 'application_tracking.html')

def interviews(request):
    return render(request, 'interviews.html')

def job_information(request, jobID):
    jobs = JobPost.objects.filter(id=jobID).first()
    return render(request, 'job_information.html', {'jobs':jobs})

def feedback(request):
    return render(request, 'feedback.html')

def logout(request):
    return render(request, 'logout.html')



