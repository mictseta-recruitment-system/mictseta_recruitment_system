from django.shortcuts import render
from jobs.models import JobPost,FeedBack,Interview
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle
from profiles.models import SupportingDocuments

# Create your views here.

def job_seeker_dashboard(request):
    return render(request, 'my_profile.html')

def my_profile(request):
    institution = Institution.objects.all()
    qualification = Qualification.objects.all()
    nqf = NQF.objects.all()
    language = LanguageList.objects.all()
    reading = ReadingProficiencyList.objects.all()
    speaking = SpeakingProficiencyList.objects.all()
    writing = WritingProficiencyList.objects.all()
    job_list = JobPost.objects.filter(status='open')
    computer = ComputerSkillsList.objects.all()
    proficiency = ComputerProficiency.objects.all()
    selected_skill = request.POST.get('skill1', '')  # Default to empty string if not set
    selected_proficiency = request.POST.get('level', '')  # Default to empty string if not set
    soft = SoftSkillsList.objects.all()
    proficiency = SoftProficiency.objects.all()
    job_title = JobTitle.objects.all()
    return render(request, 'my_profile.html',{
        'institutions':institution, 
        'qualifications':qualification,
        'nqfs':nqf,
        'languages':language,
        'readings':reading, 
        'speakings':speaking, 
        'writings':writing,
        'job_titles':job_title,
        'computers': computer,
        'proficiencys': proficiency,
        'selected_skill': selected_skill,
        'selected_proficiency': selected_proficiency,
        'softs':soft, 
        'proficiencys':proficiency
        })


def address_details(request):
    return render(request, 'address_details.html')

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
    docs = SupportingDocuments.objects.filter(user=request.user)
    return render(request, 'supporting_documents.html',{"docs":docs})

def job_details(request):
    
    return render(request, 'jobseeker_job_details.html', {'job_list':job_list})

def application_tracking(request):
    feed_back = FeedBack.objects.filter(user=request.user)
    return render(request, 'application_tracking.html',{'feedback_list':feed_back})

def interviews(request):
    return render(request, 'interviews.html')

def job_information(request, jobID):
    jobs = JobPost.objects.filter(id=jobID).first()
    return render(request, 'job_information.html', {'jobs':jobs})

def delete_feadback(request,feedbackID):
    
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



