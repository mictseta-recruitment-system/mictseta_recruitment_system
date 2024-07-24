from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect,ensure_csrf_cookie
import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User 
from .models import Task, Category
from .forms import TaskForm, CategoryForm

# Create your views here.



@csrf_protect
def create_task(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception as e:
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})
			data = {
            	'name'			:  json_data.get('task_name'),
				'category'		:  json_data.get('category'),
				'assigned_to'	:  json_data.get('assigned_to'),
				'priority'		:  json_data.get('priority'),
				'description'	:  json_data.get('description'),
				}
			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {f'{key}' :[' field is required ']}, 'status':'error'}, status=404)
			form = TaskForm(data)
			if form.is_valid() : 
				user_exist = User.objects.filter(email=data['assigned_to']).exists()
				if user_exist:
					user = User.objects.get(email=data['assigned_to'])
					category_exist = Category.objects.filter(name=data['category']).exists()
					if category_exist:
						category = Category.objects.get(name=data['category'])
						task_exist = Task.objects.filter(name=data['name'],category=category, assigned_to=user, priority=data['priority'], description=data['description']).exists()
						if not task_exist:
							task = Task.objects.create(name=data['name'],category=category, assigned_to=user, priority=data['priority'], description=data['description'])
							task.save()
							return JsonResponse({'message':f'Task {task.name} Created successfuly', 'status':'success'}, status=201) 
						else:
							return JsonResponse({'errors': {'Task':['Task Already Exists']}, 'status':'error'}, status=400)
					else:
						return JsonResponse({'errors': {'Category':['Category does not exist']}, 'status':'error'}, status=400)
				else:
					return JsonResponse({'errors': {'User':['User assigned to does not exist']}, 'status':'error'}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


@csrf_protect
def update_task(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception as e:
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})

			data = {
            	'name'			:  json_data.get('task_name'),
				'category'		:  json_data.get('category'),
				'assigned_to'	:  json_data.get('assigned_to'),
				'priority'		:  json_data.get('priority'),
				'description'	:  json_data.get('description'),
				'taskid'		:  json_data.get('taskID'),
            }

			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {'validation':[f'{key} field is required ']}, 'status':'error'}, status=404)
			form = TaskForm(data)
			if form.is_valid() : 
				user_exist = User.objects.filter(email=data['assigned_to']).exists()
				if user_exist:
					user = User.objects.get(email=data['assigned_to'])
					print(user)
					category_exist = Category.objects.filter(name=data['category']).exists()
					if category_exist:
						category = Category.objects.get(name=data['category'])
						task_exist = Task.objects.filter(name=data['name'],category=category, assigned_to=user, priority=data['priority'], description=data['description']).exists()
						if not task_exist:
							task = Task.objects.get(id=int(data['taskid']))
							task.name = data['name']
							task.category = category
							task.assigned_to = user
							task.priority = data['priority']
							task.description = data['description']
							task.save()
							return JsonResponse({'message':f'Task {task.name} Updated successfuly', 'status':'success'}, status=201) 
						else:
							return JsonResponse({'errors': {'Task':['Task Already Exists']}, 'status':'error'}, status=400)
					else:
						return JsonResponse({'errors': {'Category':['Category does not exist']}, 'status':'error'}, status=400)
				else:
					return JsonResponse({'errors': {'User':['User assigned to does not exist']}, 'status':'error'}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:       
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)


@csrf_protect
def delete_task(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception :
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})

			data = {
            	'taskID'    : json_data.get('taskID')
            }

			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {'validation':[f'{key} field is required ']}, 'status':'error'}, status=404)
            
			task_exist = Task.objects.filter(id=int(data['taskID'])).exists()
			if not task_exist:
				return JsonResponse({'errors': {'task':['task Not Found']}, 'status':'error'}, status=400)
			try:
				task = Task.objects.get(id=int(data['taskID']))
				task.delete()
				return JsonResponse({'message':f'task {task.name} Deleted successfuly', 'status':'success'}, status=201) 
			except Exception as e :
				return JsonResponse({'errors': {'Delete':[f'Error Deleting task {e}']}, 'status':'error'}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:       
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)

@csrf_protect
def check_task(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception :
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})

			data = {
            	'taskID'    : json_data.get('taskID')
            }

			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {'validation':[f'{key} field is required ']}, 'status':'error'}, status=404)
            
			task_exist = Task.objects.filter(id=int(data['taskID'])).exists()
			if not task_exist:
				return JsonResponse({'errors': {'task':['task Not Found']}, 'status':'error'}, status=400)
			try:
				task = Task.objects.get(id=int(data['taskID']))
				if task.is_complete == False:
					task.is_complete = True
				else:
					task.is_complete = False

				task.save()
				return JsonResponse({'message':f'task {task.name} status Changed successfuly', 'status':'success'}, status=201) 
			except Exception as e :
				return JsonResponse({'errors': {'Delete':[f'Error Deleting task {e}']}, 'status':'error'}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:       
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)



@csrf_protect
def create_category(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception :
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})

			data = {
            	'name'			:  json_data.get('category_name'),
            }

			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {'validation':[f'{key} field is required ']}, 'status':'error'}, status=404)
			form = CategoryForm(data)
			if form.is_valid() : 
				category_exist = Category.objects.filter(name=data['name']).exists()
				if not category_exist:	
					category = Category.objects.create(user=request.user, name=data['name'])
					return JsonResponse({'message':f'category {category.name} Created successfuly', 'status':'success'}, status=201) 
				else:
					return JsonResponse({'errors': {'Category':['Category Already Exists']}, 'status':'error'}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:       
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)

@csrf_protect
def update_category(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception :
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})

			data = {
            	'name'			:  json_data.get('category_name'),
            	'categoryID'    : json_data.get('categoryID')
            }

			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {'validation':[f'{key} field is required ']}, 'status':'error'}, status=404)
            
			category_exist = Category.objects.filter(id=int(data['categoryID'])).exists()
			if not category_exist:
				return JsonResponse({'errors': {'Category':['Category Not Found']}, 'status':'error'}, status=400)

			form = CategoryForm(data)
			if form.is_valid() : 
				category_exist = Category.objects.filter(name=data['name']).exists()
				if not category_exist:	
					category = Category.objects.get(id=int(data['categoryID']))
					category.name = data['name']
					category.save()
					return JsonResponse({'message':f'category {category.name} Updated successfuly', 'status':'success'}, status=201) 
				else:
					return JsonResponse({'errors': {'Category':['Category name is taken']}, 'status':'error'}, status=400)
			else:
				return JsonResponse({"errors":form.errors, "status":"error"}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:       
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)

@csrf_protect
def delete_category(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				json_data = json.loads(request.body)
			except Exception :
				return JsonResponse({'errors':{'request':['Supply a json oject: check documentation for more info ']}, 'status':'error'})

			data = {
            	'categoryID'    : json_data.get('categoryID')
            }

			for key, value in data.items():
				if key == None or value == None:
					return JsonResponse({'errors': {'validation':[f'{key} field is required ']}, 'status':'error'}, status=404)
            
			category_exist = Category.objects.filter(id=int(data['categoryID'])).exists()
			if not category_exist:
				return JsonResponse({'errors': {'Category':['Category Not Found']}, 'status':'error'}, status=400)
			try:
				category = Category.objects.get(id=int(data['categoryID']))
				category.delete()
				return JsonResponse({'message':f'Category {category.name} Deleted successfuly', 'status':'success'}, status=201) 
			except Exception as e :
				return JsonResponse({'errors': {'Delete':[f'Error Deleting category {e}']}, 'status':'error'}, status=400)
		else:
			return JsonResponse({'errors': {'Method':['Forbidden Method 403']}, 'status':'error'}, status=400)
	else:       
		return JsonResponse({'errors': { "authentication" : ['you are required to log in ']}, 'status':'error'}, status=403)