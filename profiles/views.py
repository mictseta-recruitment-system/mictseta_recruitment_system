from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import UpdatePersonalInformationForm, UpdateAddressInformationForm, UpdateProfileInformationForm, ImageUploadForm, AddStaffForm, UpdateStaffForm, LeaveForm

from django.contrib.auth.models import User
from authenticate.data_validator import ValidateIdNumber
from .models import Profile, PersonalInformation, AddressInformation, ProfileImage, StaffProfile, Shift, Leave, Attendance
from django.db.utils import IntegrityError
from PIL import Image as PilImage
import os
import re
from authenticate.data_validator import ValidateIdNumber

from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.utils.timezone import now
# Create your views here.

@ensure_csrf_cookie
def render_profile_page(request):
    if request.user.is_authenticated:
        return render(request,'user_profile.html')
    else:
        return redirect('render_auth_page')


@csrf_protect
def update_user_profile(request):
    if request.user.is_authenticated:

        pr = Profile.objects.all()
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
                'r_username' : f'{request.user.username}',
                'r_email' : f'{request.user.email}',
                'r_phone' : 'False'
                # 'r_idnum' : f'{request.user.profile.idnumber}'
            }
       
            for key, value in data.items():
                if key == None or value == None:
                    return JsonResponse({'errors': f'{key} field is required ', 'status':'error'}, status=404)
            form = UpdateProfileInformationForm(data)
            if form.is_valid() : 
                exist = User.objects.filter(email=data['email']).exists()
                if exist:
                    user = User.objects.get(email=data['email'])
                    if user.email == request.user.email:
                        pass
                    else:
                        raise forms.ValidationError(f"Email: {email} is already taken")

                exist = User.objects.filter(username=data['username']).exists()
                if exist:
                    user = User.objects.get(username=data['username'])
                    if user.username == request.user.username:
                        pass
                    else:
                        raise forms.ValidationError(f"Username:{username} is already taken")
                try :
                    user = User.objects.get(id=request.user.id)
                    print(user)
                    user.username = data['username']
                    user.first_name = data['first_name']
                    user.last_name = data['last_name']
                    user.email = data['email']
                    # user.password = data['password']
                   
                    user.profile.idnumber = data['idnumber']
                    user.profile.phone = data['phone']
                    user.profile.age = ValidateIdNumber(data['idnumber']).get_age()
                    user.profile.gender = ValidateIdNumber(data['idnumber']).get_gender()
                    user.profile.save()
                    user.save()
                    print("======================")
                    print(user.profile.phone)
                    return JsonResponse({'message':f'User profile for {user.username} is updated successfuly', 'status':'success'}, status=201) 
                except Exception as e:
                    return JsonResponse({'errors': f'{e}', 'status':'error'}, status=404)
            else:
                return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
        else:
            return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    else:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


@csrf_protect
def update_personal_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            personal_data = {
                'linkedin_profile' : json_data.get('linkedin_profile'),
                'personal_website' : json_data.get('personal_website'),
                'job_title'  : json_data.get('job_title'),
                'current_employer' : json_data.get('current_employer'),
                'years_of_expreince' : json_data.get('years_of_expreince'),
                'industry' : json_data.get('industry'),
                'carear_level' : json_data.get('carear_level'),
                'desired_job' : json_data.get('desired_job'),
                'job_location' : json_data.get('job_location')
                }
            personal_data_form =  UpdatePersonalInformationForm(personal_data)
            if personal_data_form.is_valid() : #and address_data_form.is_valid():
                try:
                    # address_data_form = AddressInformationForm(address_data)
                    personal_info = PersonalInformation.objects.create(user=request.user, linkedin_profile=personal_data['linkedin_profile'],personal_website=personal_data['personal_website'],job_title=personal_data['job_title'], current_employer=personal_data['current_employer'], years_of_expreince=personal_data['years_of_expreince'], industry=personal_data['industry'], carear_level=personal_data['carear_level'], desired_job=personal_data['desired_job'], job_location=personal_data['job_location'] )
                    # address_info = AddressInformation.objects.create(user=request.user, street_address_line=address_data['street_address_line'], street_address_line1=address_data['street_address_line1'], city=address_data['city'], province=address_data['province'], postal_code=address_data['postal_code'] )
                    personal_info.save()
                    # address_info.save()     
                    return JsonResponse({"message":"update personal information success"})
                except IntegrityError:
                    personal_information = PersonalInformation.objects.get(user_id=request.user.id)
                    print(personal_information)
                    personal_information.linkedin_profile = personal_data['linkedin_profile']
                    personal_information.personal_website = personal_data['personal_website']
                    personal_information.job_title = personal_data['job_title']
                    personal_information.current_employer = personal_data['current_employer']
                    personal_information.years_of_expreince = personal_data['years_of_expreince']
                    personal_information.industry = personal_data['industry']
                    personal_information.carear_level = personal_data['carear_level']
                    personal_information.desired_job = personal_data['desired_job']
                    personal_information.job_location = personal_data['job_location']
                    personal_information.save()
                    print('=========done=========')
                    return JsonResponse({"message":"update personal information success", "status":"success"}, status=200)
                except Exception as e: 
                    return JsonResponse({'errors':f'{e}', 'status':'error'}, status=404)
            else:
               return JsonResponse({"errors":personal_data_form.errors, "status":"error"}, status=400) 
        else:
            return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    else:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)



@csrf_protect
def update_address_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'})
            address_data = {
                'street_address_line' : json_data.get('street_address_line'),
                'street_address_line1' : json_data.get('street_address_line1'),
                'city'  : json_data.get('city'),
                'province' : json_data.get('province'),
                'postal_code' : json_data.get('postal_code')
                
                }
            
            address_data_form =  UpdateAddressInformationForm(address_data)
            if address_data_form.is_valid() : #and address_data_form.is_valid():
                try:
            
                    address_info = AddressInformation.objects.create(user=request.user, street_address_line=address_data['street_address_line'], street_address_line1=address_data['street_address_line1'], city=address_data['city'], province=address_data['province'], postal_code=address_data['postal_code'] )
                    address_info.save()     
                    return JsonResponse({"message":"update personal information success"})
                except IntegrityError:
                    address_information = AddressInformation.objects.get(user_id=request.user.id)
                    print(address_information)
                    address_information.street_address_line = address_data['street_address_line']
                    address_information.street_address_line1 = address_data['street_address_line1']
                    address_information.city = address_data['city']
                    address_information.province = address_data['province']
                    address_information.postal_code = address_data['postal_code']
                   
                    address_information.save()
                    print('=========done=========')
                    return JsonResponse({"message":"update personal information success", "status":"success"}, status=200)
                except Exception as e: 
                    return JsonResponse({'errors':f'{e}', 'status':'error'}, status=404)
            else:
               return JsonResponse({"errors":address_data_form.errors, "status":"error"}, status=400) 
        else:
            return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
    else:       
        return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@csrf_protect
def upload_profile_image(request):
    if request.method == 'POST':

        try:
            image = request.FILES['image']
            empID = empID = request.POST['empID']
            print(request.POST)
            print(empID)
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
                    print(file_to_delete)
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

    return working_hours

def calculate_salary(rate, working_hours):
    salary = rate * working_hours * 20
    return salary

@csrf_protect
def add_staff(request):
    if request.user.is_authenticated:
        current_time = now()
        for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
            if leave.start_date <= current_time <= leave.end_date:
                return HttpResponse("Request denied: you are on leave")
        if request.user.is_superuser:
 
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
                    'password' : json_data.get('password'),
                    'password2' : json_data.get('password'),
                    'is_superuser' : json_data.get('super'),
                    'is_staff' : json_data.get('staff'),
                    'salary' : json_data.get('salary'),
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


                form = AddStaffForm(data)
                if form.is_valid() : 
                    exist = User.objects.filter(email=data['email']).exists()
                    if exist:
                        raise forms.ValidationError(f"Email: {email} is already taken")

                    exist = User.objects.filter(username=data['username']).exists()
                    if exist:
                        raise forms.ValidationError(f"Username:{username} is already taken")
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
                else:
                    return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
            else:
                return JsonResponse({'errors': 'Forbidden 403', 'status':'error'}, status=400)
        else:       
            return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    else:
        return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)


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
                            exist = User.objects.get(email=data['email']) 
                            if user != exist:
                                exist = None
                        except:
                            exist = None
                        if exist is not None:
                            pass
                        else:
                            return JsonResponse({"errors":f"phone:{data['email']} is already taken", "status":"error"}, status=400)

                        try:
                            exist = User.objects.get(username=data['username']) 
                        except:
                            exist = None
                        if exist is not None:
                            pass
                        else:
                            return JsonResponse({"errors":f"phone:{data['username']} is already taken", "status":"error"}, status=400)
                        
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

def get_late(shift_start):
    
    # Define the first time with seconds
    

    # Convert the first time to minutes since midnight
    hours1, minutes1, seconds1 = map(int, shift_start.split(":"))
    total_minutes1 = hours1 * 60 + minutes1 + seconds1 / 60

    # Get the current time
    now = datetime.now()

    # Convert the current time to minutes since midnight
    total_minutes_now = now.hour * 60 + now.minute + now.second / 60

    # Calculate the difference
    difference = total_minutes_now - total_minutes1
    
    if difference > 0 :
        late = True
    else:
        late = False
        difference = 0
    return (late, round(difference))

def mark_attendence(request, empID):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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
            return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)
    else:
        return JsonResponse({'errors': { "Unauthorized" : ['You dont have the The Permission to make this request']}, 'status':'error'}, status=403)

def end_attendace(request, empID):
    from django.utils import timezone
    if request.user.is_authenticated:
        if request.user.is_superuser:
 
            if request.method == 'GET':
                try:
                    employee = User.objects.get(id=int(empID))
                    today = timezone.now().date()
                    att = Attendance.objects.get(employee=employee, date=timezone.now().date())
                    att.active = "Inactive"
                    att.save()
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
        current_time = now()
        for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
            if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
                return HttpResponse("<h1>Request denied: you are on leave</h1>")
        if request.user.is_staff:

            try:
                leave = Leave.objects.get(id=int(leaveID))
                leave.status = "Closed"
                leave.save()
                return redirect(request.META.get('HTTP_REFERER', '/'))

            except Exception as e:
                return HttpResponse(f'close leave : {e}')
        else:       
            return HttpResponse('You dont have the The Permission to make this request')
    else:
        return HttpResponse('you are required to log')

def approve_leave(request, leaveID):
    if request.user.is_authenticated:
        current_time = now()
        for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
            if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
                return HttpResponse("<h1>Request denied: you are on leave</h1>")
        if request.user.is_staff:

            try:
                leave = Leave.objects.get(id=int(leaveID))
                leave.status = "Approved"
                leave.save()
                return redirect(request.META.get('HTTP_REFERER', '/'))

            except Exception as e:
                return HttpResponse(f'approve leave : {e}')
        else:       
            return HttpResponse('You dont have the The Permission to make this request')
    else:
        return HttpResponse('you are required to log')

def reject_leave(request, leaveID):
    if request.user.is_authenticated:
        current_time = now()
        for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
            if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
                return HttpResponse("<h1>Request denied: you are on leave</h1>")
        if request.user.is_staff:

            try:
                leave = Leave.objects.get(id=int(leaveID))
                leave.status = "Rejected"
                leave.save()
                return redirect(request.META.get('HTTP_REFERER', '/'))

            except Exception as e:
                return HttpResponse(f'reject leave : {e}')
        else:       
            return HttpResponse('You dont have the The Permission to make this request')
    else:
        return HttpResponse('you are required to log')

def seen_leave(request, leaveID):
    if request.user.is_authenticated:
        current_time = now()
        for leave in request.user.leave_set.all():  # Ensure you call the method and use the correct related name
            if leave.start_date <= current_time <= leave.end_date and leave.status == "Approved":
                return HttpResponse("<h1>Request denied: you are on leave</h1>")
        if request.user.is_staff:
            try:
                leave = Leave.objects.get(id=int(leaveID))
                leave.seen = True
                leave.save()
                return redirect(request.META.get('HTTP_REFERER', '/'))

            except Exception as e:
                return HttpResponse(f'seen leave : {e}')
        else:       
            return HttpResponse('You dont have the The Permission to make this request')
    else:
        return HttpResponse('you are required to log')