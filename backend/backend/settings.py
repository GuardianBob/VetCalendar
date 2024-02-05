"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv("DEBUG", "False") == "True"
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

host_list = [
    'http://localhost:9000',
    'http://127.0.0.1:9000',
    'http://127.0.0.1:8000',
    'http://localhost',
    "https://jgmeyer.dev",
    "https://vetcal.jgmeyer.dev",
    "https://vss.jgmeyer.dev",
    "https://vssb.jgmeyer.dev",
    "https://vss-dev.jgmeyer.dev",
    "https://vssb-dev.jgmeyer.dev",
    "https://jbear-creations.com", 
    "https://jbearcreations.com",
]

ALLOWED_HOSTS = [
    '*'
    # 'http://localhost',
    # 'localhost',
    # '127.0.0.1',
    # 'jbearlocal.com',
    # "jbear-creations.com", 
    # "jbearcreations.com",
    # "vcb.jgmeyer.dev",  # MUST INCLUDE DOMAIN to avoid CORS issues
    # "vetcal.jgmeyer.dev",  # MUST INCLUDE DOMAIN to avoid CORS issues
    # "vss-dev.jgmeyer.dev",  # MUST INCLUDE DOMAIN to avoid CORS issues
    # "vssb-dev.jgmeyer.dev",  # MUST INCLUDE DOMAIN to avoid CORS issues
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:9000',
    'http://*.127.0.0.1',
    'http://*.127.0.0.1:9000',
    'http://*.127.0.0.1:8000',
    'http://192.168.2.16:9000',
    'http://localhost',
    "https://jgmeyer.dev", 
    "https://jbear-creations.com", 
    "https://jbearcreations.com",
    "https://vetcal.jgmeyer.dev",
    "https://vcb.jgmeyer.dev",
    "https://vss-dev.jgmeyer.dev",
    "https://vssb-dev.jgmeyer.dev",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_NAME = 'csrftoken'

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

CORS_ALLOWED_ORIGINS = host_list
    
# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:9000',
#     'http://localhost:9000/*',
#     'http://*.127.0.0.1',
#     'http://*.127.0.0.1:8000/*',
#     'http://*.127.0.0.1:9000/*',
#     'http://192.168.2.16:9000/*',
#     "https://jgmeyer.dev/*", 
#     "https://jbear-creations.com/*", 
#     "https://jbearcreations.com/*",
#     "https://vetcal.jgmeyer.dev/*",
#     "https://vcb.jgmeyer.dev/*",
#     "https://vss-dev.jgmeyer.dev/*",
#     "https://vssb-dev.jgmeyer.dev/*",
# ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'VetCalendar',
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'backend.urls'

AUTH_USER_MODEL = 'login.User'
AUTHENTICATION_BACKENDS = ['login.backends.EmailBackend']

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

# CORS_ALLOW_CREDENTIALS: True 

# CORS_ALLOW_HEADERS = [
#     'X-CSRF-TOKEN',
#     'XCSRF-TOKEN',
#     'HTTP_X_CSRFTOKEN',
#     'HTTP_X_XSRF_TOKEN',
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [], # local
        'DIRS': [os.path.join(BASE_DIR,'templates')], #cPanel
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

WSGI_APPLICATION = 'backend.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'logfile.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv('DEVELOPMENT_MODE') == "True":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }
    # CSRF_COOKIE_DOMAIN = None
    # CSRF_COOKIE_SECURE = False # Set this to True if you are using HTTPS
    # CSRF_COOKIE_HTTPONLY = False # Set this to True if you are using 
else:
    DATABASES = {
        'default': { # MySQL Settings
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_TABLE'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASS'),
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {  
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
            }
        }
    }
    # CSRF_COOKIE_DOMAIN = CORS_ORIGIN_WHITELIST
    # CSRF_COOKIE_SECURE = True # Set this to True if you are using HTTPS


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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE =  'UTC'
TIME_ZONE =  'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     'VetCalendar/static/',
#     # 'ShiftScheduler/static/',
# ]
STATIC_ROOT = os.path.join(BASE_DIR, "static") #local
# STATIC_ROOT = os.path.join(BASE_DIR, 'public') # cPanel

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "tmp") # cPanel

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
