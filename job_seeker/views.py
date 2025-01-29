from django.shortcuts import render, redirect
from jobs.models import JobPost,FeedBack,Interview, Quiz, QuizResults
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency, Institution, Qualification,NQF, JobTitle
from profiles.models import SupportingDocuments, WorkingExpereince
from django.db.models import Count
# Create your views here.


def count_profile(req):

    score = 0

    if req.user.first_name and req.user.first_name != " " and req.user.first_name != "" :
        score += 1
    if req.user.last_name and req.user.last_name != " "  and req.user.last_name != "":
        score += 1
    if req.user.profile.cover_letter and req.user.profile.cover_letter != " " and req.user.profile.cover_letter != "":
        score += 1
    if req.user.profile.phone and req.user.profile.phone != " " and req.user.profile.phone != "":
        score += 1
    if req.user.profile.race and req.user.profile.race != " " and req.user.profile.race != "":
        score += 1
    if req.user.profile.maritial_status and req.user.profile.maritial_status != " " and req.user.profile.maritial_status != "" :
        score += 1
    if req.user.profile.disability and req.user.profile.disability != " " and req.user.profile.disability != "" :
        score += 1
    if req.user.profile.linkedin_profile and req.user.profile.linkedin_profile != " " and req.user.profile.linkedin_profile != "" :
        score += 1
    if req.user.profile.personal_website and req.user.profile.personal_website != " " and req.user.profile.personal_website != "" :
        score += 1

    total = (score/9) * 100
    return round(total) 

def count_language(req):

    score = 0
    lang = req.user.language_set.all()
    if len(lang) > 0 :
        score += 1
    if len(lang) > 1 :
        score += 1
    total = (score/2) * 100
    return round(total) 

def count_address(req):
    score = 0
    
    # Ensure user has an address before accessing its fields
    if hasattr(req.user, 'address') and req.user.address:
        if req.user.address.street_address_line and req.user.address.street_address_line.strip():
            score += 1
        if req.user.address.city and req.user.address.city.strip():
            score += 1
        if req.user.address.province and req.user.address.province.strip():
            score += 1
        if req.user.address.postal_code and req.user.address.postal_code.strip():
            score += 1
    
    # Calculate the percentage
    total = (score / 4) * 100
    return round(total)


def count_academic(req):
    score = 0
    academics = req.user.qualifications.all()

    if len(academics) == 0:
        return 0  # Return 0 if there are no academic records

    for academic in academics:
        if academic.institution and academic.institution != " " and academic.institution != "":
            score += 1
        if academic.field_of_study and academic.field_of_study != " " and academic.field_of_study != "":
            score += 1
        if academic.nqf_level and academic.nqf_level != " " and academic.nqf_level != "":
            score += 1
        if academic.start_date and academic.start_date != " " and academic.start_date != "":
            score += 1
        if academic.end_date and academic.end_date != " " and academic.end_date != "":
            score += 1
        if academic.status and academic.status != " " and academic.status != "":
            score += 1

    total = (score / (6 * len(academics))) * 100
    return round(total)


def count_cs(req):

    score = 0
    cs = req.user.computerskills_set.all()
    if len(cs) > 0 :
        score += 1
    if len(cs) > 1 :
        score += 1
    if len(cs) > 2 :
        score += 1
    if len(cs) > 3 :
        score += 1
    if len(cs) > 4 :
        score += 1
   
    total = (score/5) * 100
    return round(total) 

def count_ss(req):

    score = 0
    cs = req.user.softskills_set.all()
    if len(cs) > 0 :
        score += 1
    if len(cs) > 1 :
        score += 1
    if len(cs) > 2 :
        score += 1
    if len(cs) > 3 :
        score += 1
    if len(cs) > 4 :
        score += 1

    total = (score/5) * 100
    return round(total) 

def count_doc(req):
    score = 0
    cs = req.user.documents.all()
    if len(cs) > 0 :
        score += 1
    total = (score/1.1) * 100
    return round(total) 

def job_seeker_dashboard(request):
    institution = Institution.objects.all()
    qualification = Qualification.objects.all()
    nqf = NQF.objects.all()
    language = LanguageList.objects.all()
    reading = ReadingProficiencyList.objects.all()
    speaking = SpeakingProficiencyList.objects.all()
    writing = WritingProficiencyList.objects.all()
   
    computer = ComputerSkillsList.objects.all()
    proficiency = ComputerProficiency.objects.all()
    selected_skill = request.POST.get('skill1', '')  # Default to empty string if not set
    selected_proficiency = request.POST.get('level', '')  # Default to empty string if not set
    soft = SoftSkillsList.objects.all()
    proficiency = SoftProficiency.objects.all()
    job_title = JobTitle.objects.all()

    working_experience = WorkingExpereince.objects.filter(user=request.user).all()

    print('--------------------------------------------------')
    print(institution)
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
        'proficiencys':proficiency,
        'working_experiences':working_experience,
        'stat_profile': count_profile(request),
        'stat_lang': count_language(request),
        'stat_address':count_address(request),
        'stat_academic':count_academic(request),
        'stat_soft':count_ss(request),
        'stat_comp':count_cs(request),
        'stat_doc':count_doc(request)
        })

def my_profile(request):
    institution = Institution.objects.all()
    qualification = Qualification.objects.all()
    nqf = NQF.objects.all()
    language = LanguageList.objects.all()
    reading = ReadingProficiencyList.objects.all()
    speaking = SpeakingProficiencyList.objects.all()
    writing = WritingProficiencyList.objects.all()
   
    computer = ComputerSkillsList.objects.all()
    proficiency = ComputerProficiency.objects.all()
    selected_skill = request.POST.get('skill1', '')  # Default to empty string if not set
    selected_proficiency = request.POST.get('level', '')  # Default to empty string if not set
    soft = SoftSkillsList.objects.all()
    proficiency = SoftProficiency.objects.all()
    job_title = JobTitle.objects.all()
    working_experience = WorkingExpereince.objects.filter(user=request.user).all()
    print('--------------------------------------------------')
    print(institution)
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
        'proficiencys':proficiency,
       'working_experiences':working_experience
        })



def cv(request):
    return render(request, 'cv.html')
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

def generate_cv(request):
    # Define the context for the template
    context = {
        'user': request.user,
        # Add any additional data you need in the template
    }

    # Render the template to an HTML string
    html_string = render_to_string('cv.html', context)

    # Generate the PDF
    pdf = HTML(string=html_string).write_pdf()

    # Return the PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cv.pdf"'
    return response



def address_details(request):
    return render(request, 'address_details.html')



def hiring_process(request):
    return render(request, 'hiring_process.html')


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
    job_list = JobPost.objects.filter(status='open')
    return render(request, 'jobseeker_job_details.html', {'job_list':job_list})

def application_tracking(request):
    feed_back = FeedBack.objects.filter(user=request.user)
    jobs = JobPost.objects.filter(jobapplication__user__id=request.user.id).annotate(feedback_count=Count('feedback')).filter(feedback_count__gt=0)

    return render(request, 'application_tracking.html',{'feedback_list':feed_back, 'jobs':jobs})

def interviews(request):
    return render(request, 'interviews.html')

def job_information(request, jobID):
    jobs = JobPost.objects.filter(id=jobID).first()
    return render(request, 'job_information.html', {'jobs':jobs})

def quiz_test(request, jobID):
    job = JobPost.objects.filter(id=int(jobID)).first()
    if job:
        try:
            quiz = Quiz.objects.get(job=job)
        except Exception as e:
            return render(request, 'error_quiz.html')
        quiz_results = QuizResults.objects.filter(user=request.user, quiz=quiz).first()
        if quiz_results:
             return render(request, 'done_quiz.html')
        if quiz :
            return render(request, 'quiz_test.html', {'quiz':quiz,'jobID':jobID})
        else:
            return redirect('job_application', jobID=job.id)
    return redirect('job_information', jobID=jobID)

def delete_feadback(request,feedbackID):    
    feed_back = FeedBack.objects.filter(user=request.user)
    feed_back_delete = FeedBack.objects.filter(id=int(feedbackID)).first()
    feed_back_delete.delete()
    return render(request, 'application_tracking.html',{'feedback_list':feed_back})


def feedback(request):
    if request.user.is_authenticated:
        interviews = Interview.objects.filter(user=request.user)
    
        return render(request, 'feedback.html',{ 'interviews':interviews})


def logout(request):
    return render(request, 'logout.html')



