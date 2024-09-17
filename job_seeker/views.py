from django.shortcuts import render
from jobs.models import JobPost, SkillValidation, FeedBack,Interview
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle
from profiles.models import SupportingDocuments
# Create your views here.
def job_seeker_dashboard(request):
    return render(request, 'job_seeker_dashboard.html')

def personal_details(request):
    return render(request, 'personal_details.html')


def address_details(request):
    return render(request, 'address_details.html')

def academic_qualifications(request):
    institution = Institution.objects.all()
    qualification = Qualification.objects.all()
    nqf = NQF.objects.all()
    return render(request, 'academic_qualifications.html', {'institutions':institution, 'qualifications':qualification,'nqfs':nqf})

def language_proficiency(request):
    language = LanguageList.objects.all()
    reading = ReadingProficiencyList.objects.all()
    speaking = SpeakingProficiencyList.objects.all()
    writing = WritingProficiencyList.objects.all()
    print(language)
    print(reading)
    print(speaking)
    return render(request, 'language_proficiency.html',{'languages':language,'readings':reading, 'speakings':speaking, 'writings':writing})

def soft_skills(request):
    soft = SoftSkillsList.objects.all()
    proficiency = SoftProficiency.objects.all()
    return render(request, 'soft_skills.html', {'softs':soft, 'proficiencys':proficiency})

def computer_skills(request):
    computer = ComputerSkillsList.objects.all()
    proficiency = ComputerProficiency.objects.all()
    return render(request, 'computer_skills.html', {'computers':computer, 'proficiencys':proficiency})

def working_experience(request):
    job_title = JobTitle.objects.all()
    return render(request, 'working_experience.html', {'job_titles':job_title})

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



