# Django Project Setup Guide

This guide provides step-by-step instructions to set up and run a Django project on your local machine.

## Table of Contents


1. [Clone the Repository](#clone-the-repository)
2. [Install Dependencies](#install-dependencies)
3. [Running the Development Server](#running-the-development-server)
4. [Using the Routes signin & signup](#Using-the-routes-signin-&-signup)

## Clone the Repository

Clone the project repository from GitHub to your local machine:

```sh

git clone https://github.com/ethanux/mictseta_recruitment_system.git
```
Navigate to the projects root directory
```sh
cd your-django-project
```

## Install Dependencies

while you are in the projects directory, install the project dependencies:

```sh

pip install -r requirements.txt
```

## Running the Development Server

Start the development server by running:

```sh

python manage.py runserver
```

The server will start at http://127.0.0.1:8000/. Open this URL in your web browser to view the project.

## Using the Routes

To use the routes signin and signup , you need to send a Post request and the paylaod must be in json format.
- For signin json payload example 
	```sh
	url       :https://127.0.0.1:8000/auth/signin
	method    : POST
	data-type : json-format 
	{
		"email": "your email here",
		"password": "your password here"
	}

	```
- For registering json payload example 
	```sh
	url       :https://127.0.0.1:8000/auth/signup
	method    : POST
	data-type : json-format 
	{
		"username" : "username here", 
		"first_name" : "first name here",
		"last_name" : "last name here",
		"email" : "email here",
		"password" : "password here",
		"password2" : "confirm password here"
	}

	```

After Each Request
The Server willl return a respones data in json formart 

-  if the request is not successfull or something went wrong the server will return the follwing structure
```sh
	{
		"errors" : {
					"field_name": ['error message'],
				},
		"status" : "error"
	}
```
- if the request is successful, the server will return the following structure
```ssh
	{
		"message" : " success message here" , 

		"status" : "success"
	}
```