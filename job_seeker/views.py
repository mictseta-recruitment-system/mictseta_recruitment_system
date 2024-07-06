from django.shortcuts import render

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
    return render(request, 'jobseeker_job_details.html')



