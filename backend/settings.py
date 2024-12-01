"""
Django settings for backend project.
"""

from pathlib import Path
from datetime import timedelta
import pymysql

import os
import logging

# Configure MySQL driver

pymysql.install_as_MySQLdb()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'didierherlin18@gmail.com'  # Adresse Gmail
EMAIL_HOST_PASSWORD = 'tgmo jtix kakn cupe'  # Mot de passe d'application
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_TIMEOUT = 30  # Timeout en secondes



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(_file_).resolve().parent.parent

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# api google fichier json
GOOGLE_DRIVE_CREDS_JSON = os.path.join(BASE_DIR, 'datadriveapi-437607-6bb13dde471d.json')

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-xmyy56c+#c$!7u^#8#&(egh&2_+or##y4+t)xps)i#zbhlw(5o')  # Use environment variable for security
DEBUG = os.environ.get('DEBUG', 'True') == 'True'  # Use environment variable for debugging

ALLOWED_HOSTS = ["127.0.0.1",'localhost', ".vercel.app", ".now.sh"]

# CORS configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    
]


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['content-type', 'authorization']
CORS_ALLOW_ALL_METHODS = True

# Logging configuration
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('django.security.csrf').setLevel(logging.DEBUG)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'api',
    'RapportApp',
    'ProjetApp',
    'ArchiveApp',
    'NotificationApp',
    'GoocleDriveApi',
    'rest_framework.authtoken',
    'rest_framework_simplejwt'
    
]

# Middleware configuration
MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'api.middleware.UserRoleMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'NAME': os.environ.get('DB_NAME', 'gestion_rapport'),  # Use environment variable
        'USER': os.environ.get('DB_USER', 'root'),  # Use environment variable
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),  # Use environment variable
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# JWT and REST framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',  # Si vous utilisez l'authentification par token
    ],
}


# settings.py


from datetime import timedelta

SIMPLE_JWT = {

    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,

    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Access token valid for 7 days
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),  # Refresh token valid for 90 days
    'ROTATE_REFRESH_TOKENS': True,  # Generate a new refresh token when refreshing an access token
    'BLACKLIST_AFTER_ROTATION': False,  # Don't blacklist old refresh tokens, allowing multiple refresh tokens
    'UPDATE_LAST_LOGIN': False,  # Disable updating last login to reduce database writes


    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',

}

# # Internationalization settings

#     'USER_ID_CLAIM': 'user_id',
#     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#     'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

#     'JTI_CLAIM': 'jti',

#     'SLIDING_TOKEN_LIFETIME': timedelta(days=7),  # Sliding token valid for 7 days
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=90),  # Sliding refresh token valid for 90 days

#     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     'SLIDING_TOKEN_REFRESH_CLAIM': 'refresh',
# }


CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
