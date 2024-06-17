
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import re
# Create your views here.

@csrf_protect
def get_all_users_page(request):
    if request.user.is_authenticated:
        users = User.objects.all()
        return render(request,'users.html', {'users':users})
    return redirect('render_auth_page')

@csrf_protect
def get_user(request, username):
    user = User.objects.get(username=username)
    return render(request,'user_profile.html', {'get_user':user})


def serialize_users(Users):
    users = []

    for User in Users :
        user = {
            "username": User.username,
            "first_name": User.first_name,
            "last_name": User.last_name,
            "email": User.email,
            "is_staff": User.is_staff,
            "date_joined" : User.date_joined,
           
            "personal_information": {},
            "address_information" : {},

        }
        try:
            profile = {
                "idnumber":User.profile.idnumber,
                    "phone": User.profile.phone,
                    "gender":User.profile.gender,
                    "age":User.profile.age
            }
            user.update({"profile" : profile})
        except:
            user.update({"profile" : {}})

        try:
            personal_information = {
                    "linkedin_profile":User.personalinformation.linkedin_profile,
                    "personal_website":User.personalinformation.personal_website,
                    "job_title":User.personalinformation.job_title,
                    "current_employer":User.personalinformation.current_employer,
                    "years_of_expreince":User.personalinformation.years_of_expreince,
                    "industry":User.personalinformation.industry,
                    "carear_level":User.personalinformation.carear_level,
                    "desired_job":User.personalinformation.desired_job,
                    "job_location":User.personalinformation.job_location,
            }
            user.update({"personal_information" : personal_information})
        except:
            user.update({"personal_information" : {}})
             

        try:
            address_information = {
                    "street_address_line":User.addressinformation.street_address_line,
                    "street_address_line1":User.addressinformation.street_address_line1,
                    "city":User.addressinformation.city,
                    "province":User.addressinformation.province,
                    "postal_code":User.addressinformation.postal_code,
            }
            user.update({"address_information" : address_information})
        except:
            user.update({"address_information" : {}})

        users.append(user)
    return users



@csrf_protect
def get_users(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
            filter_ = json_data.get('filter')
            if filter_ == "all":
                try:
                    users = User.objects.all()
                except Exception as e:
                    return JsonResponse({'errors':f'{e}', 'status':'error'}, status=400)
                
                users = serialize_users(users)
                return JsonResponse({'message': f'User List','users':users, 'status': 'success'}, status=200)
               
            
            elif filter_ == "username":
                username = json_data.get('username')

                if username == "" or username == None or not username:
                    return JsonResponse({'errors':'username is not provided', 'status':'error'}, status=400)

                if " " in username:
                    return JsonResponse({'errors':'no spaces allowed', 'status':'error'}, status=400)
                pattern = r"[~`+!@#$%^&*()=\-/\*\\|}{\[\];'\?]"
                matches = re.findall(pattern, username)
                if matches:
                    return JsonResponse({'errors':'special characters not allowed', 'status':'error'}, status=400)
                if len(username) < 3 :
                    return JsonResponse({'errors':'username is short', 'status':'error'}, status=400)
                exist = User.objects.filter(username=username).exists()
                if not exist:
                    return JsonResponse({'errors':'username does not exist', 'status':'error'}, status=400)
                user = User.objects.get(username=username)
                user = serialize_users([user])
                return JsonResponse({'message': f'User List','user':user, 'status': 'success'}, status=200)
            else:
                return JsonResponse({'errors':'Invalid filter', 'status':'error'}, status=400)
        else:
            return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)
    else:
        return JsonResponse({'errors': 'you are not logged in', 'status': 'error'}, status=400)


#========================================================================================================================================================
@csrf_protect
def delete_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
            except Exception :
                return JsonResponse({'errors':'Supply a json oject: check documentation for more info ', 'status':'error'}, status=400)
            username = json_data.get('username')
            if username == "" or username == None or not username:
                return JsonResponse({'errors':'username is not provided', 'status':'error'}, status=400)

            if " " in username:
                return JsonResponse({'errors':'no spaces allowed', 'status':'error'}, status=400)
            pattern = r"[~`+!@#$%^&*()=\-/\*\\|}{\[\];'\?]"
            matches = re.findall(pattern, username)
            if matches:
                return JsonResponse({'errors':'special characters not allowed', 'status':'error'}, status=400)
            if len(username) < 3 :
                return JsonResponse({'errors':'username is short', 'status':'error'}, status=400)
            exist = User.objects.filter(username=username).exists()
            if not exist:
                return JsonResponse({'errors':'username does not exist', 'status':'error'}, status=400)
            user = User.objects.get(username=username)
            user.delete()
            return JsonResponse({'message': 'User deleted successfuly', 'status': 'success'}, status=200)
        else:
            return JsonResponse({'errors': 'Invalid request method', 'status': 'error'}, status=400)
    else:
        return JsonResponse({'errors': 'you are not logged in', 'status': 'error'}, status=400)