from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UpdateQualificationForm, UpdateAddressInformationForm,UpdateWorkingExpereinceForm, UpdateProfileInformationForm, ImageUploadForm, AddStaffForm, UpdateStaffForm, LeaveForm
from config.models import LanguageList, SpeakingProficiencyList,ReadingProficiencyList,WritingProficiencyList,ComputerSkillsList,ComputerProficiency,SoftSkillsList, SoftProficiency,NQF, Institution, Qualification, JobTitle

from django.contrib.auth.models import User
from authenticate.data_validator import ValidateIdNumber
from .models import Profile,Reference, AddressInformation, ProfileImage, StaffProfile, Shift, Leave, Attendance, Education,Language,ComputerSkills, SoftSkills,SupportingDocuments,WorkingExpereince
from django.db.utils import IntegrityError
from PIL import Image as PilImage
import os
import re
from authenticate.data_validator import ValidateIdNumber

from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.utils.timezone import now

from PIL import Image
from PyPDF2 import PdfReader
import mimetypes
import io
# Create your views here.

@ensure_csrf_cookie
def render_profile_page(request):
    if request.user.is_authenticated:
        return render(request,'user_profile.html')
    else:
        return redirect('render_auth_page')

ALLOWED_EXTENSIONS = ['png', 'jpeg', 'jpg','pdf']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rename_document(filename, file_type, req):
    filename = f"{req.user.profile.idnumber}-{file_type}" + "." + filename.rsplit('.', 1)[1].lower()
    return filename
def calculate_working_hours(start_time, end_time): 
    time_format = "%H:%M:%S"
    try:
        start = datetime.strptime(start_time, time_format)
        end = datetime.strptime(end_time, time_format)
    except ValueError:
        
        return JsonResponse({'errors':{'time' :["Time format should be HH:mm:ss"]}, 'status':'error'})
    
    if end <= start:
        return JsonResponse({'errors':{'time' :["End time must be greater than start time"]}, 'status':'error'})
    delta = end - start
    working_hours = delta.total_seconds() / 3600.0  # Convert seconds to hours

    return round(working_hours)

def calculate_salary(rate, working_hours):
    salary = rate * working_hours * 20
    return salary

def get_late(shift_start):
    # Convert the first time to minutes since midnight
    hours1, minutes1, seconds1 = map(int, shift_start.split(":"))
    total_minutes1 = hours1 * 60 + (minutes1+10) + seconds1 / 60
    # Get the current time
    now = datetime.now()
    # Convert the current time to minutes since midnight
    total_minutes_now = now.hour * 60 + now.minute + now.second / 60
    # Clculate the difference
    difference = total_minutes_now - total_minutes1
    if difference > 0 :
        late = True
    else:
        late = False
        difference = 0
    return (late, round(difference))

@csrf_protect
def update_user_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    data = {
        'linkedin_profile' : json_data.get('linkedin_profile'),
        'personal_website' : json_data.get('personal_website'),
        'first_name' : json_data.get('first_name'),
        'last_name' : json_data.get('last_name'),
        'email' : json_data.get('email'),
        'phone' : json_data.get('phone'),
        'idnumber': json_data.get('idnumber'),
        'maritial_status' : json_data.get('maritial_status'),
        'race' : json_data.get('race'),
        'disability' : json_data.get('disability'),
        'cover_letter':json_data.get('cover_letter'),
        'r_username' : f'{request.user.username}',
        'r_email' : f'{request.user.email}',
        'r_phone' : 'False',
        }
    shallow_copy = data.copy()
    for key,value in shallow_copy.items():
        if value == "" or value == " " or value=='None':
            shallow_copy[key] = "empty"
    #form = UpdateProfileInformationForm(data)
    #if not form.is_valid() : 
        #return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
    exist = User.objects.filter(email=data['email']).exists()
    if exist:
        user = User.objects.get(email=data['email'])
        if not user.email == request.user.email:
            raise forms.ValidationError(f"Email: {email} is already taken")
    try :
        user = User.objects.get(id=request.user.id)
        user.username = data['idnumber']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.profile.idnumber = data['idnumber']
        user.profile.phone = data['phone']
        user.profile.maritial_status = data['maritial_status']
        user.profile.race = data['race']
        user.profile.disability = data['disability']
        user.profile.age = ValidateIdNumber(data['idnumber']).get_age()
        user.profile.gender = ValidateIdNumber(data['idnumber']).get_gender()
        user.profile.dob = ValidateIdNumber(data['idnumber']).get_gender()
        user.profile.cover_letter = data['cover_letter']
        user.profile.linkedin_profile = data['linkedin_profile']
        user.profile.save()
        user.save()
        return JsonResponse({'message':f'User profile for {user.username} is updated successfuly', 'status':'success'}, status=201) 
    except Exception as e:
        return JsonResponse({'errors': f'{e}', 'status':'error'}, status=404)
    

@csrf_protect
def update_qualification(request):
    if not request.user.is_authenticated:      
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    data = {
        'institution'  : json_data.get('institution'),
        'field_of_study' : json_data.get('field_of_study'),
        'nqf_level' : json_data.get('nqf_level'),
        'start_date' : json_data.get('start_date'),
        'end_date' : json_data.get('end_date'),
        'status' : json_data.get('status')
    }

    # qualification_data_form =  UpdateQualificationForm(data)
    # if not qualification_data_form.is_valid() : #and address_data_form.is_valid():
    #     return JsonResponse({"errors":qualification_data_form.errors, "status":"error"}, status=400) 
    institution = Institution.objects.get(id=int(data['institution']))
    field_of_study = Qualification.objects.get(id=int(data['field_of_study']))
    nqf_level = NQF.objects.get(id=int(data['nqf_level']))

    try:
        exists = Education.objects.filter(institution=institution,user=request.user).exists()
        if exists:
            return JsonResponse({'errors':{ "Qualification" : ['it Already exists']}, 'status':'error'}, status=404)
        education = Education.objects.create(user=request.user,institution=institution,field_of_study=field_of_study,nqf_level=nqf_level,start_date=data['start_date'],end_date=data['end_date'],status=data['status'])
        education.save()
        return JsonResponse({"message":"Added qualification information success", 'status':'success'})
    except Exception as e: 
        return JsonResponse({'errors':f'{e}', 'status':'error'}, status=404)
  

@csrf_protect
def update_language(request):
    if not request.user.is_authenticated:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    
    data = {
        'language' : json_data.get('language'),
        'reading_proficiency' : json_data.get('reading_proficiency'),
        'writing_proficiency' : json_data.get('writing_proficiency'),
        'speaking_proficiency' : json_data.get('speaking_proficiency'),
    }
            
    language = LanguageList.objects.get(id=int(data['language']))
    reading_proficiency = ReadingProficiencyList.objects.get(id=int(data['reading_proficiency']))
    writing_proficiency = WritingProficiencyList.objects.get(id=int(data['writing_proficiency']))
    speaking_proficiency = SpeakingProficiencyList.objects.get(id=int(data['speaking_proficiency']))

    exists = Language.objects.filter(user=request.user,language=language,reading_proficiency=reading_proficiency,writing_proficiency=writing_proficiency,speaking_proficiency=speaking_proficiency).exists()
    if exists:
        return JsonResponse({'errors':{ "Languge" : ['it Already exists']}, 'status':'error'}, status=400)
    # ##language_data_form =  UpdateLanguageForm(data)
    # if not language_data_form.is_valid() : 
    #            return JsonResponse({"errors":language_data_form.errors, "status":"error"}, status=400) 
               
    language = Language.objects.create(user=request.user,language=language,reading_proficiency=reading_proficiency,writing_proficiency=writing_proficiency,speaking_proficiency=speaking_proficiency)
    language.save()
    return JsonResponse({"message":"Added Language information ", 'status':'success'})
           

@csrf_protect
def update_computer_skill(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            
    data = {
        'skill' : json_data.get('skill'),
        'level' : json_data.get('level'),
    }
    skill = ComputerSkillsList.objects.get(id=int(data['skill']))
    proficiency = ComputerProficiency.objects.get(id=int(data['level']))
    #skill_data_form =  UpdateSkillsForm(data)
            # if skill_data_form.is_valid() : #and address_data_form.is_valid():
            # else:
            #     return JsonResponse({"errors":skill_data_form.errors, "status":"error"}, status=400) 
    exists = ComputerSkills.objects.filter(user=request.user,skill=skill,proficiency=proficiency).exists()
    if exists:
        return JsonResponse({'errors':{ "Skill" : ['it Already exists']}, 'status':'error'}, status=404)
    skill = ComputerSkills.objects.create(user=request.user,skill=skill,proficiency=proficiency)
    skill.save()
    return JsonResponse({"message":"Added Skill information success", 'status':'success'})

@csrf_protect
def update_soft_skill(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            
    data = {
        'skill' : json_data.get('skill'),
        'level' : json_data.get('level'),
    }
    skill = SoftSkillsList.objects.get(id=int(data['skill']))
    proficiency = SoftProficiency.objects.get(id=int(data['level']))

    #skill_data_form =  UpdateSkillsForm(data)
            # if skill_data_form.is_valid() : #and address_data_form.is_valid():
            # else:
            #     return JsonResponse({"errors":skill_data_form.errors, "status":"error"}, status=400) 
    exists = SoftSkills.objects.filter(user=request.user,skill=skill,proficiency=proficiency).exists()
    if exists:
        return JsonResponse({'errors':{ "Skill" : ['it Already exists']}, 'status':'error'}, status=404)
    skill = SoftSkills.objects.create(user=request.user,skill=skill,proficiency=proficiency)
    skill.save()
    return JsonResponse({"message":"Added Skill information success", 'status':'success'})


@csrf_protect
def update_address_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)      

    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    address_data = {
        'street_address_line' : json_data.get('street'),
        'city'  : json_data.get('city'),
        'province' : json_data.get('province'),
        'postal_code' : json_data.get('postal_code')
    }
            
    address_data_form =  UpdateAddressInformationForm(address_data)
    if not address_data_form.is_valid() : 
        return JsonResponse({"errors":address_data_form.errors, "status":"error"}, status=400)      
    try:        
        address_info = AddressInformation.objects.create(user=request.user, street_address_line=address_data['street_address_line'], city=address_data['city'], province=address_data['province'], postal_code=address_data['postal_code'] )
        address_info.save()     
        return JsonResponse({"message":"update personal information success", "status":"success"}, status=200)
    except IntegrityError:
        address_information = AddressInformation.objects.get(user_id=request.user.id)
        address_information.street_address_line = address_data['street_address_line']
        address_information.city = address_data['city']
        address_information.province = address_data['province']
        address_information.postal_code = address_data['postal_code']         
        address_information.save()
        return JsonResponse({"message":"update personal information success", "status":"success"}, status=200)
    except Exception as e: 
            return JsonResponse({'errors':f'{e}', 'status':'error'}, status=404)

@csrf_protect
def update_working_experince(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)      

    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
    working_experience = {
        'job_title' : json_data.get('job_title'),
        'company'  : json_data.get('company'),
        'location' : json_data.get('location'),
        'start_date' : json_data.get('start_date'),
        'end_date' : json_data.get('end_date'),
        'description' : json_data.get('description')
    }
            
    #working_experience_form =  UpdateWorkingExpereinceForm(working_experience)
    #if not working_experience_form.is_valid() : 
    #    return JsonResponse({'errors': working_experience_form.errors, 'status': 'error'}, status=400)
    job_title = JobTitle.objects.get(id=int(working_experience['job_title']))

    exists = WorkingExpereince.objects.filter(job_title=job_title, user=request.user).exists()
    if exists:
        wk = WorkingExpereince.objects.get(job_title=job_title, user=request.user)
        wk.job_title = job_title
        wk.company = working_experience['company']
        wk.location = working_experience['location']
        wk.start_date = working_experience['start_date']
        wk.end_date = working_experience['end_date']
        wk.description=working_experience['description']
        wk.save()
        return JsonResponse({'message':"working experince updated successfully",'status':'success'}, status=201)
    wk = WorkingExpereince.objects.create(
        job_title=job_title, 
        user=request.user, 
        company=working_experience['company'],
        location=working_experience['location'],
        start_date=working_experience['start_date'],
        end_date=working_experience['end_date'],
        description=working_experience['description']
        )   
    wk.save()
    return JsonResponse({"message":"update working experince information success", "status":"success"}, status=200)

@csrf_protect
def update_reference(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})    
    data = {
        'working_expereince': json_data.get('working_expereince'),
        'full_name' : json_data.get('full_name'),
        'phone' : json_data.get('phone'),
        'position' : json_data.get('position'),
    }
    working_expereince = WorkingExpereince.objects.get(id=int(data['working_expereince']))
    exists = Reference.objects.filter(user=request.user,working_experince=working_expereince).exists()
    if exists:
        reference = Reference.objects.get(user=request.user,working_experince=working_expereince)
        reference.full_name = data['full_name']
        reference.phone = data['phone']
        reference.position = data['position']
        reference.save()
        return JsonResponse({"message":"updated Reference information success", 'status':'success'}, status=200)
    reference = Reference.objects.create(user=request.user,working_experince=working_expereince, full_name=data['full_name'], phone=data['phone'], position=data['position'])
    reference.save()
    return JsonResponse({"message":"Added Reference information success", 'status':'success'}, status=201)



def upload_supporting_document(request):
    if request.method == 'POST':
       return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)
    try:
        document = request.FILES['document']
        document_type = request.POST['type']
    except Exception as e:
        return JsonResponse({'errors': 'No selected file', 'status': 'error'}, status=400)
    try: 
        max_file_size = 3 * 1024 * 1024  # 3 MB in bytes
        if document.size > max_file_size:
            return JsonResponse({'errors': 'File size exceeds 3 MB limit', 'status': 'error'}, status=400)
        # Verify if file is an image or PDF
        allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        mime_type, _ = mimetypes.guess_type(document.name)

        if mime_type not in allowed_mime_types:
            return JsonResponse({'errors': 'Only image or PDF files are allowed', 'status': 'error'}, status=400)

            # Verify the file format for images and PDFs
        try:
            if mime_type.startswith('image/'):
                # Verify the image file format
                img = Image.open(document)
                img.verify()  # Verifies that the image is valid
            elif mime_type == 'application/pdf':
                # Verify the PDF file format
                pdf = PdfReader(io.BytesIO(document.read()))
                if pdf.numPages < 1:  # If no pages, it's not a valid PDF
                    raise ValueError('Invalid PDF file')
            else:
                return JsonResponse({'errors': 'Unsupported file format', 'status': 'error'}, status=400)
        except Exception as e:
            return JsonResponse({'errors': f'File format verification failed: {str(e)}', 'status': 'error'}, status=400)

        if allowed_file(document.name) == False: 
            return JsonResponse({'errors':'File type not allowed', 'status': 'error'}, status=400)
        try:
            exists = SupportingDocuments.objects.filter()
            document.name = rename_document(document.name, document_type,request)
            exists = SupportingDocuments.objects.filter(document="static/supportindocuments/documents/"+document.name,document_type=document_type).exists()
            if exists:
                return JsonResponse({'errors': 'Document Already Exists', 'status': 'error'}, status=400)
            supporting_document = SupportingDocuments.objects.create(user=request.user,document=document, document_type=document_type) 
            supporting_document.save()
            return JsonResponse({'message': 'Image uploaded successfully', 'status': 'success'}, status=201)
        except Exception as e:
            return JsonResponse({'errors': e, 'status': 'error'}, status=400)
    except (IOError, SyntaxError):
        return JsonResponse({'errors': 'Invalid image file', 'status': 'error'}, status=400)
   


@ensure_csrf_cookie
def delete_supporting_document(request, document_id):
    if request.method == 'GET':
        try:
            supporting_document = SupportingDocuments.objects.get(id=document_id, user=request.user)
            supporting_document.document.delete() 
            supporting_document.delete()
            docs = SupportingDocuments.objects.filter(user=request.user)
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_reference(request,reference_id):
    if request.method == 'GET':
        try:
            reference = Reference.objects.get(id=reference_id)
            reference.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_working_experince(request,working_experince_id):
    if request.method == 'GET':
        try:
            working_experince = WorkingExpereince.objects.get(id=working_experince_id)
            working_experince.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_address_info(request,address_info_id):
    if request.method == 'GET':
        try:
            address_info = AddressInformation.objects.get(id=address_info_id)
            address_info.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_soft_skill(request,soft_skill_id):
    if request.method == 'GET':
        try:
            soft_skill = SoftSkills.objects.get(id=soft_skill_id)
            soft_skill.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_computer_skill(request,computer_skill_id):
    if request.method == 'GET':
        try:
            computer_skill = ComputerSkills.objects.get(id=computer_skill_id)
            computer_skill.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_qualification(request,qualification_id):
    if request.method == 'GET':
        try:
            qualification = Education.objects.get(id=qualification_id)
            qualification.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

@ensure_csrf_cookie
def delete_language(request,language_id):
    if request.method == 'GET':
        try:
            language = Language.objects.get(id=language_id)
            language.delete()
            return redirect('my_profile')
        except Exception as e:
            return JsonResponse({'errors': str(e), 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)



@csrf_protect
def upload_profile_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            empID =  request.POST['empID']
            # return JsonResponse({'errors': {'file' :['Bad Request']}, 'status': 'error'}, status=400)
        except Exception as e:
            return JsonResponse({'errors': f'{e}', 'status': 'error'}, status=400)
        try:
            if not image or image.name == '':
                return JsonResponse({'errors':'No selected file', 'status': 'error'}, status=400)
            if not image and not allowed_file(image.filename):
                return JsonResponse({'errors':'File type not allowed', 'status': 'error'}, status=400)
            img = PilImage.open(image)
            img.verify()  # Verify that this is a valid image
            # If user does not select a file, the browser submits an empty file without a filename
            try:
                user = User.objects.get(id=int(empID))
                profile_image = ProfileImage.objects.create(user=user,image=image) 
                profile_image.save()
                return JsonResponse({'message': 'Image uploaded successfully', 'status': 'success'}, status=201)
            except:
                user_profile_image = ProfileImage.objects.get(user=request.user)

                if user_profile_image:
                    ext= user_profile_image.image.path.split('/')[-1].split('_')[-1].split('.')[-1]
                    name = user_profile_image.image.path.split('/')[-1].split('_')[0:-1]
                    if type(name) is type(list('jeff')):
                        name = '_'.join(name)
                    filename = name+'.'+ext
                    files = user_profile_image.image.path.split('/')
                    files[-1] = filename
                    file_to_delete = '/'.join(files)
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)

                    user_profile_image.image.delete()
                    user_profile_image.image = image
                    user_profile_image.save()
                    return JsonResponse({'message': 'Image uploaded successfully', 'status': 'success'}, status=201)
                else:
                    return JsonResponse({'errors': 'NOT FOUND', 'status': 'error'}, status=400)

        except (IOError, SyntaxError):
            return JsonResponse({'errors': 'Invalid image file', 'status': 'error'}, status=400)
        else:
            return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)
    return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)

#==================================================================================================================================


@csrf_protect
def add_staff(request):
    if not request.user.is_authenticated:    
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    if not request.user.is_superuser:
        return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)

    if not request.method == 'POST':
        return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    try:
        json_data = json.loads(request.body)
    except Exception :
        return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
        
    current_time = now()
    for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
        if leave.start_date <= current_time <= leave.end_date:
            return HttpResponse("Request denied: you are on leave")
    
    data = {
        'username' : json_data.get('username'),
        'first_name' : json_data.get('first_name'),
        'last_name' : json_data.get('last_name'),
        'email' : json_data.get('email'),
        'phone' : json_data.get('phone'),
        'idnumber': json_data.get('idnumber'),
        'job_title' : json_data.get('job_title'),
        'department' : json_data.get('department'),
        'password' : json_data.get('password'),
        'password2' : json_data.get('password'),
        'is_superuser' : json_data.get('super'),
        'is_staff' : json_data.get('staff'),
        'salary' : json_data.get('salary'),
        'rate' : json_data.get('rate'),
        'start_time' : json_data.get('start_time'),
        'end_time' : json_data.get('end_time'),
        }
    for key, value in data.items():
        if key == None or value == None:
            return JsonResponse({'errors': f'{key} field is required ', 'status':'error'}, status=404)
                
    if data['is_superuser'] == 'True':
        is_user_superuser = True
    else:
        is_user_superuser = False   
    if data['is_staff'] == 'True':
        is_user_staff = True
    else:
        is_user_staff = False

    form = AddStaffForm(data)
    if not form.is_valid() : 
        return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
    email_exist = User.objects.filter(email=data['email']).exists()
    if email_exist:
        return JsonResponse({'errors': f'Email: {email_exist} is already taken', 'status':'error'}, status=404)
    username_exist = User.objects.filter(username=data['username']).exists()
    if username_exist:
        return JsonResponse({'errors': f'Username:{username_exist} is already taken', 'status':'error'}, status=404)
    try :
        user = User.objects.create(username=data['username'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'],password=make_password(data['password']), is_superuser=is_user_superuser, is_staff=is_user_staff)
        staff = StaffProfile.objects.create(user=user,job_title=data['job_title'],department=data['department'],salary=calculate_salary(int(data['rate']), calculate_working_hours(data['start_time'], data['end_time'])),phone=data['phone'], idnumber=data['idnumber'], gender=ValidateIdNumber(data['idnumber']).get_gender(),age=ValidateIdNumber(data['idnumber']).get_age(), dob=ValidateIdNumber(data['idnumber']).get_birthdate())
        shift = Shift.objects.create(employee=user,rate=data['rate'],start_time=data['start_time'],end_time=data['end_time'], working_hours=calculate_working_hours(data['start_time'], data['end_time']))
        user.save()
        staff.save()
        shift.save()
        return JsonResponse({'message':f'Staff profile for {user.first_name} {user.last_name} is updated successfuly', 'status':'success'}, status=201) 
    except Exception as e:
        return JsonResponse({'errors': f'{e}', 'status':'error'}, status=404)
   

@csrf_protect
def update_staff(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            current_time = now()
            for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
                if leave.start_date <= current_time <= leave.end_date:
                    return HttpResponse("Request denied: you are on leave")
            if request.method == 'POST':
                try:
                    json_data = json.loads(request.body)
                except Exception :
                    return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
                print(json_data)
                data = {
                    'username' : json_data.get('username'),
                    'first_name' : json_data.get('first_name'),
                    'last_name' : json_data.get('last_name'),
                    'email' : json_data.get('email'),
                    'phone' : json_data.get('phone'),
                    'idnumber': json_data.get('idnumber'),
                    'job_title' : json_data.get('job_title'),
                    'department' : json_data.get('department'),
                    'is_superuser' : json_data.get('super'),
                    'is_staff' : json_data.get('staff'),
                    'salary' : json_data.get('salary'),
                    'password' : 'default1',
                    'password2' : 'default1',
                    'rate' : json_data.get('rate'),
                    'start_time' : json_data.get('start_time'),
                    'end_time' : json_data.get('end_time'),
                   
                    # 'r_idnum' : f'{request.user.profile.idnumber}'
                }
                for key, value in data.items():
                    if key == None or value == None:
                        return JsonResponse({'errors': f'{key} field is required ', 'status':'error'}, status=404)
                
                if data['is_superuser'] == 'True':
                    is_user_superuser = True
                else:
                    is_user_superuser = False
                
                if data['is_staff'] == 'True':
                    is_user_staff = True
                else:
                     is_user_staff = False


                form = UpdateStaffForm(data)
                if form.is_valid() : 
                    exist = User.objects.filter(staffprofile__idnumber=data['idnumber']).exists()
                    if exist:
                        user = User.objects.get(staffprofile__idnumber=data['idnumber'])
                        
                        try:
                            exist = User.objects.filter(email=data['email']).exists()
                            if exist :
                                user_by_email = User.objects.get(email=data['email'])
                                if user != user_by_email:
                                    return JsonResponse({"errors":f"email:{data['email']} is already taken", "status":"error"}, status=400)
                            else:
                                pass
                        except Exception as e:
                                    return JsonResponse({"errors":{'data':[f'e']}, "status":"error"}, status=400)
                        try:
                            exist = User.objects.filter(username=data['username']).exists()
                            if exist :
                                user_by_username = User.objects.get(username=data['username'])
                                if user != user_by_username:
                                    return JsonResponse({"errors":f"username:{data['username']} is already taken", "status":"error"}, status=400)
                            else:
                                pass
                        except Exception as e:
                                    return JsonResponse({"errors":{'data':[f'e']}, "status":"error"}, status=400)                        
                        try:
                            exist = User.objects.filter(staffprofile__phone=data['phone'], id=data['idnumber']).exists()
                            if not exist:
                                pass
                            else: 
                                exist = User.objects.get(staffprofile__phone=data['phone'])
                                if user == exist:
                                    pass
                                else: 
                                    return JsonResponse({"errors":f"phone:{data['phone']} is already taken", "status":"error"}, status=400)
                        except Exception as e:
                            return JsonResponse({"errors":f'{e}', "status":"error"}, status=400)
                        
                    else:
                        return JsonResponse({"errors":f'User:staff Uer does not exist', "status":"error"}, status=400)

                    try :
                        user = User.objects.get(staffprofile__idnumber=data['idnumber'])
                        user.first_name = data['first_name']
                        user.last_name = data['last_name']
                        user.email = data['email']
                        # user.password = data['password']
                        user.staffprofile.job_title = data['job_title']
                        user.staffprofile.phone = data['phone']
                        user.staffprofile.department = data['department']
                        user.staffprofile.salary = calculate_salary(int(data['rate']), calculate_working_hours(data['start_time'], data['end_time']))
                        user.shift.rate = data['rate']
                        user.shift.start_time = data['start_time']
                        user.shift.end_time = data['end_time']
                        user.shift.working_hours = calculate_working_hours(data['start_time'], data['end_time'])
                        user.staffprofile.save()
                        user.shift.save()
                        user.save()
                        return JsonResponse({'message':f'Staff profile for {user.first_name} {user.last_name} is updated successfuly', 'status':'success'}, status=201) 
                    except Exception as e:
                        return JsonResponse({'errors': f'{e}', 'status':'error'}, status=404)
                else:
                    return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
            else:
                return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
        else:       
            return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    else:
        return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)



def mark_attendence(request, empID):
    if request.user.is_authenticated:
        if request.user.is_staff:
            from django.utils import timezone
            if request.method == 'GET':
                try:
                    employee = User.objects.get(id=int(empID))
                    is_late, minutes = get_late(employee.shift.start_time)
                    exists = Attendance.objects.filter(employee=employee, date=timezone.now().date()).exists()
                    if exists:
                        attendance = Attendance.objects.get(employee=employee, date=timezone.now().date())
                        attendance.active = "Active"
                        attendance.save()
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                    else:
                        attendance = Attendance.objects.create(employee=employee, shift=employee.shift, status="Present", is_late=is_late, minutes=minutes, active="Active")
                        attendance.save()
                        return redirect(request.META.get('HTTP_REFERER', '/'))
                
                except Exception as e:
                    return JsonResponse({'errors':{'mark': [f'{e}']}, 'status':'error'})

                return JsonResponse({'errors': { "leave" : ['not yet done']}, 'status':'error'}, status=403)
            else:
                return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
        else:       
            return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)
    else:
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)

def end_attendace(request, empID):
    from django.utils import timezone
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
 
            if request.method == 'GET':
                try:
                    employee = User.objects.get(id=int(empID))
                    today = timezone.now().date()
                    try:
                        att = Attendance.objects.get(employee=employee, date=timezone.now().date())
                        att.active = "Inactive"
                        att.save()
                        return JsonResponse({'message': 'Session Complete successfully, waiting for next session' , 'status':'success'})
                    except Exception :
                        return JsonResponse({'message': 'Session Complete successfully, waiting for next session' , 'status':'success'})
                except Exception as e:
                    return JsonResponse({'errors':{'mark': [f'{e}']}, 'status':'error'})

                return JsonResponse({'errors': { "leave" : ['not yet done']}, 'status':'error'}, status=403)
            else:
                return JsonResponse({'errors': 'Ivalid request method', 'status':'error'}, status=400)
        else:       
            return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    else:
        return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)

def leave(request):
    if request.user.is_authenticated:
        current_time = now()
        for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
            if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
                return HttpResponse("Request denied: you are on leave")
        if request.user.is_staff:
 
            if request.method == 'POST':
                try:
                    json_data = json.loads(request.body)
                except Exception :
                    return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})

                data = {
                    'leave_type' : json_data.get('leave_type'),
                    'message' : json_data.get('message'),
                    'start_date' : json_data.get('start_date'),
                    'end_date' : json_data.get('end_date'),
                }

                for key, value in data.items():
                    if key == None or value == None:
                        return JsonResponse({'errors': f'{key} field is required ', 'status':'error'}, status=404)

                form = LeaveForm(data)
                if form.is_valid() :
                    leave_exists = Leave.objects.filter(employee=request.user, lave_type=data['leave_type'], message=data['message'], start_date=data['start_date'], end_date=data['end_date']).exists()
                    if leave_exists:
                        return JsonResponse({"errors":{'Leave':['It already Exists']}, "status":"error"}, status=400)
                    leave = Leave.objects.create(employee=request.user, lave_type=data['leave_type'], message=data['message'], start_date=data['start_date'], end_date=data['end_date'], status="Pending")
                    return JsonResponse({'message':f'Leave request submited successfuly waiting managers approval', 'status':'success'}, status=201) 
                    
                else:
                    return JsonResponse({"errors":form.errors, "status":"error"}, status=400) 
            else:
                return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
        else:       
            return JsonResponse({'errors': { "Leave" : ['you are required to log in ']}, 'status':'error'}, status=403)
    else:
        return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)

def close_leave(request, leaveID):
    if request.user.is_authenticated:
        return HttpResponse('you are required to log')
    if request.user.is_staff:
        return HttpResponse('You dont have the The Permission to make this request')
    current_time = now()
    for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
        if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
            return HttpResponse("<h1>Request denied: you are on leave</h1>")
    try:
        leave = Leave.objects.get(id=int(leaveID))
        leave.status = "Closed"
        leave.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        return HttpResponse(f'close leave : {e}')

def approve_leave(request, leaveID):
    if request.user.is_authenticated:
        return HttpResponse('you are required to log')
    if request.user.is_staff:
        return HttpResponse('You dont have the The Permission to make this request')
    current_time = now()
    for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
        if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
            return HttpResponse("<h1>Request denied: you are on leave</h1>")
    try:
        leave = Leave.objects.get(id=int(leaveID))
        leave.status = "Approved"
        leave.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        return HttpResponse(f'approve leave : {e}')

def reject_leave(request, leaveID):
    if request.user.is_authenticated:
        return HttpResponse('you are required to log')
    if request.user.is_staff:
        return HttpResponse('You dont have the The Permission to make this request')
    current_time = now()
    for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
        if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
            return HttpResponse("<h1>Request denied: you are on leave</h1>")
    try:
        leave = Leave.objects.get(id=int(leaveID))
        leave.status = "Rejected"
        leave.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        return HttpResponse(f'reject leave : {e}')


def seen_leave(request, leaveID):
    if request.user.is_authenticated:
        return HttpResponse('you are required to log')
    if request.user.is_staff:
        return HttpResponse('You dont have the The Permission to make this request')
    current_time = now()
    for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
        if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
            return HttpResponse("<h1>Request denied: you are on leave</h1>")
    try:
        leave = Leave.objects.get(id=int(leaveID))
        leave.seen = True
        leave.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Exception as e:
        return HttpResponse(f'seen leave : {e}')
             