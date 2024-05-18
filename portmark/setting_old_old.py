
import os
from pathlib import Path
import django_heroku

import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.contrib.messages import constants as messages
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ux4%%570r*q0c1v22!u^=ht(9*!+y)=r37)h2#k!0b-xeox@_f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'admin_argon.apps.AdminArgonConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'giftweb',
    'accounts',
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.humanize',
    'cloudinary',
    'cloudinary_storage'

    #'activity_log'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'activity_log.middleware.ActivityLogMiddleware'
]

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = "/accounts/login/"
#ACTIVITYLOG_EXCLUDE_URLS = ('/admin/activity_log/activitylog', )

ROOT_URLCONF = 'portmark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'giftweb.custom_context_processors.notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'portmark.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'Firstwork51a51$',
        'HOST': 'db.uvnrhzftedoooliigwqm.supabase.co',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,  # Change this to your desired minimum password length
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# settings.py
"""
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Use your actual Redis server URL
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
"""
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
django_heroku.settings(locals())

MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success',
    messages.ERROR: 'alert-danger',
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.AccountNoBackend',
    'accounts.backends.CustomAuthBackend',
)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cloudinary configuration

cloudinary.config( 
  cloud_name = "dwpqoubdw", 
  api_key = "746427962229227", 
  api_secret = "Mw778m_arBap_WKexphIdoar0dw" 
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': "dwpqoubdw",  # Replace with os.getenv('CLOUDINARY_CLOUD_NAME')
    'API_KEY': "746427962229227",  # Replace with os.getenv('CLOUDINARY_API_KEY')
    'API_SECRET': "Mw778m_arBap_WKexphIdoar0dw",  # Replace with os.getenv('CLOUDINARY_API_SECRET')
}

# CKEditor settings
CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_JQUERY_URL = "https://code.jquery.com/jquery-3.6.0.min.js"  # You can use the jQuery version you prefer
CKEDITOR_IMAGE_BACKEND = "pillow"  # Use Pillow for image processing

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'toolbar': 'all',
        'extraPlugins': ','.join([
            'codesnippet',
            'widget',
            'dialog',
            'html5video',
            'youtube',  # Add the 'youtube' plugin here
        ]),
        'filebrowserImageUploadUrl': '/ckeditor/upload/',  # This is the URL for image uploads
        'filebrowserUploadUrl': '/ckeditor/upload/',  # This is the URL for file uploads
    }
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



# Use the SMTP backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Set your Elastic Email SMTP server settings
EMAIL_HOST = 'smtp.elasticemail.com'
EMAIL_PORT = 2525  # Use Elastic Email's SMTP port
EMAIL_HOST_USER = 'format@formatguy.store'  # Your Elastic Email username
EMAIL_HOST_PASSWORD = '6B4FAB6724F3EC3A70CB423515A64C29E62F'  # Your Elastic Email password
EMAIL_USE_TLS = True  # Use TLS for a secure connection
