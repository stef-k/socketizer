"""
Django settings for socketizer project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
# Use WhiteNoise for static files handling
from whitenoise import WhiteNoise
from .common import secret_variable

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_variable('settings', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Staying simple, use one settings file with conditional statements
DEVELOPMENT = True

# Allowed hosts
if DEVELOPMENT:
    ALLOWED_HOSTS = []
else:
    # Hosts and Domains that are valid for this site
    ALLOWED_HOSTS = ['socketizer.com']

# Application definition
# Common apps
DJANGO_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Let WhiteNoise handle static files in development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    # Django allauth
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',
    # Django Rest Framework
    # 'rest_framework',
    # Django storages
    'storages'
]

PROJECT_APPS = [

    'mainsite',

    # User Profile app
    'userprofiles',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS
# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'socketizer.contrib.sites.migrations'
}
# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be above all middleware except Django's security
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# URLs CONFIGURATION
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'socketizer.urls'
# TEMPLATES CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # scan each project directory for a "templates" sub directory
            os.path.join(
                BASE_DIR, 'socketizer', 'templates'),
        ],
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
# WSGI APPLICATION CONFIGURATION
# ------------------------------------------------------------------------------
WSGI_APPLICATION = 'socketizer.wsgi.application'
# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
# ------------------------------------------------------------------------------
# MEDIA AND STATIC FILES CONFIGURATION
# # Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# ------------------------------------------------------------------------------
if not DEVELOPMENT:
    # S3 settings
    AWS_STORAGE_BUCKET_NAME = \
        secret_variable.secret_variable('s3', 'AWS_STORAGE_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = \
        secret_variable.secret_variable('s3', 'AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = \
        secret_variable.secret_variable('s3', 'AWS_SECRET_ACCESS_KEY')

    # Tell django-storages that when coming up with the URL for an item in S3
    # storage just use this domain plus the path.
    AWS_S3_CUSTOM_DOMAIN = '{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'.format(
        AWS_STORAGE_BUCKET_NAME=AWS_STORAGE_BUCKET_NAME
    )
    # ABOUT STATIC FILES: Static files are handled by WhiteNoise, see
    # http://whitenoise.evans.io/en/stable/ which is better solution from S3
    # You can remove WhiteNoise and enable the follow to let S3 handle them.
    # Our STATIC files will live at:
    # https://AWS_S3_CUSTOM_DOMAIN/STATIC_FILES_LOCATION.s3.amazonaws.com
    # Our MEDIA files will live at:
    # https://AWS_S3_CUSTOM_DOMAIN/MEDIA_FILES_LOCATION.s3.amazonaws.com
    # Tell the staticfiles app to use S3Boto storage when writing the collected
    # static files (when you run `collectstatic`).
    #
    # STATICFILES_LOCATION = 'static'
    # STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    # STATIC_URL = 'https://{AWS_S3_CUSTOM_DOMAIN}/{
    # STATICFILES_LOCATION}/'.format(
    #     AWS_S3_CUSTOM_DOMAIN=AWS_S3_CUSTOM_DOMAIN,
    #     STATICFILES_LOCATION=STATICFILES_LOCATION,
    # )
    # # MEDIA files...
    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIA_URL = 'https://{AWS_S3_CUSTOM_DOMAIN}/{' \
                'DEFAULT_FILE_STORAGE}/'.format(
        AWS_S3_CUSTOM_DOMAIN=AWS_S3_CUSTOM_DOMAIN,
        DEFAULT_FILE_STORAGE=DEFAULT_FILE_STORAGE,
    )

    # Header cache expiry
    AWS_HEADERS = {
    # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }
else:
    # Static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(os.path.dirname(BASE_DIR),
                     'socketizer',
                     'socketizer',
                     'static'),
    )

    # Media files
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
# ------------------------------------------------------------------------------
# DATABASE CONFIGURATION
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# ------------------------------------------------------------------------------
# PostgreSQL

if DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'socketizer',
            'USER': secret_variable('database', 'USER'),
            'PASSWORD': secret_variable('database', 'PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': '5433',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'socketizer',
            'USER': secret_variable('database', 'USER'),
            'PASSWORD': secret_variable('database', 'PASSWORD'),
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# ------------------------------------------------------------------------------
# PASSWORD VALIDATION CONFIGURATION
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]
# ------------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION
DEFAULT_FROM_EMAIL = \
    'socketizer <info@socketizer.com>'

ADMINS = (
    ("""stef kariotidis""", 'stef.kariotidis@gmail.com'),
)
if DEVELOPMENT:
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = 'in-v3.mailjet.com'
    EMAIL_HOST_USER = \
        secret_variable('mailjet', 'EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = \
        secret_variable('mailjet', 'EMAIL_HOST_PASSWORD')
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
# THIRD PARTY CONFIGURATION
# ------------------------------------------------------------------------------
# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'
# ------------------------------------------------------------------------------
# ALL AUTH CONFIGURATION
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
# Make email verification mandatory to avoid junk email accounts
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ------------------------------------------------------------------------------
# django-crontab cron jobs
# To add all jobs python manage.py crontab add
# To remove all python manage.py crontab remove
# To show all jobs python manage.py crontab show
# For more see https://github.com/kraiz/django-crontab
CRONJOBS = [
    # Run every day at 00:00
    ('00 00 * * *', 'socketizer.cron.sample_function'),
]

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/mylog.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django_request.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
