"""
Django settings for mictseta_recruitment_system project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

from datetime import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+5d78i2gower*d@*0r3cl-q^r&@n=y8(m!kau8-4)q0-rw073$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['058a-102-64-32-230.ngrok-free.app','127.0.0.1', '192.168.1.195','localhost','10.0.2.2']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'dbbackup',
    'authenticate',
    'home',
    'profiles',
    'users',
    'jobs',
    'dashboard',
    'job_seeker',
    'task_manager',
    'easyaudit',
    'rest_api',
    'rest_framework',
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework.authtoken',    
    'rest_framework_simplejwt.token_blacklist',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    # 'mictseta_recruitment_system.middleware.CsrfCookieMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication', 
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
     
}
ROOT_URLCONF = 'mictseta_recruitment_system.urls'
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-csrftoken',
    'x-requested-with',
    'csrfmiddlewaretoken',
    'csrftoken',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
# # Ensure CSRF_COOKIE_HTTPONLY is True for enhanced security
# CSRF_COOKIE_HTTPONLY = False

# # Ensure CSRF_COOKIE_SECURE is True if using HTTPS
# CSRF_COOKIE_SECURE = True

# # Set CSRF_TRUSTED_ORIGINS if you have specific trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://058a-102-64-32-230.ngrok-free.app',
    'http://192.168.1.195:8000',
     'http://127.0.0.1:8000'

 ]

# # Ensure CSRF_USE_SESSIONS is True to use CSRF tokens stored in session
# CSRF_USE_SESSIONS = True

# # Ensure CSRF_FAILURE_VIEW is set to handle CSRF failures
# # CSRF_FAILURE_VIEW = 'your_app.views.csrf_failure'  # Replace with your actual view name

# # Ensure CSRF_COOKIE_SAMESITE is 'Strict' or 'Lax' based on your requirements
# CSRF_COOKIE_SAMESITE = 'Strict'

CORS_ORIGIN_ALLOW_ALL = True
# # CSRF_TRUSTED_ORIGINS = ['https://058a-102-64-32-230.ngrok-free.app']

# # settings.py



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mictseta_recruitment_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME':'database',
    #     'USER' : 'root',
    #     'PASSWORD' : 'kali',
    #     'HOST' : "127.0.0.1",
    #     "PORT" : "3306",
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

}
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location' : f'{BASE_DIR}/backup/database/'}


#DBBACKUP_FILENAME_TEMPLATE = f"Backup-{datetime.now().strftime('%H_%M_%S-%d_%m_%Y')}.backup"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'  # Or any other time zone



USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SITE_ID = 1 
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'setamict@gmail.com'
EMAIL_HOST_PASSWORD = 'owwa msaz ueit juum'
DEFAULT_FROM_EMAIL = 'setamict@gmail.com'

#after the user have registered an account it will direct the user to this endpoint 
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'rest_api/auth/login/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'rest_api/auth/login/' 

#after the user clicks on the link this will happen  


ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email' 
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True 
# AUTH_USER_MODEL ='authenticate.Users'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# DEFAULT_FROM_EMAIL = ''

