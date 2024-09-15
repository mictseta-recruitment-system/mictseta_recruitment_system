from django.shortcuts import render
from jobs.models import JobPost, SkillValidation, FeedBack,Interview
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
    return render(request, 'language_proficiency.html')

def soft_skills(request):
    skills = SkillValidation.objects.filter(category="soft")

    return render(request, 'soft_skills.html', {'skills':skills})

def computer_skills(request):
    return render(request, 'computer_skills.html')

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
    if request.user.is_authenticated:
        feed_back = FeedBack.objects.filter(user=request.user)
    return render(request, 'application_tracking.html',{'feedback_list':feed_back})

def interviews(request):
    return render(request, 'interviews.html')

def job_information(request, jobID):
    jobs = JobPost.objects.filter(id=jobID).first()
    return render(request, 'job_information.html', {'jobs':jobs})

def delete_feadback(request,feedbackID):
    if request.user.is_authenticated:
        feed_back = FeedBack.objects.filter(user=request.user)
        feed_back_delete = FeedBack.objects.filter(id=int(feedbackID)).first()
        feed_back_delete.delete()
    return render(request, 'feedback.html',{'feedback_list':feed_back})


def feedback(request):
    if request.user.is_authenticated:
        interviews = Interview.objects.filter(user=request.user)
    
    return render(request, 'feedback.html',{ 'interviews':interviews})


def logout(request):
    return render(request, 'logout.html')



