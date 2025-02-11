"""
Django settings for Sistema project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
"""ALLOWED_HOSTS = ['8ad3-200-14-226-170.ngrok-free.app']
CSRF_TRUSTED_ORIGINS = [
    'https://8ad3-200-14-226-170.ngrok-free.app',  # Dominio específico de ngrok
    'https://*.ngrok-free.app',  # Permite cualquier subdominio de ngrok
]"""
#si no se esta utilizando el host borrar o comentar para evitar este error (Invalid HTTP_HOST header: '127.0.0.1:8000'. You may need to add '127.0.0.1' to ALLOWED_HOSTS.)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q(%tm=1)sj=$)iknc_u&68ww(r^r*_^m@^_r3(j17jmm5q*060'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'Datos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Sistema.urls'

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

WSGI_APPLICATION = 'Sistema.wsgi.application'
# Configuración de almacenamiento de mensajes
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Humedal',
        'USER':'postgres',
        'PASSWORD': 'refrigerador',
        'HOST': 'localhost',
        'PORT': '5432'
    },
    'espejo': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'humedal_espejo',
        'USER': 'postgres',
        'PASSWORD': 'refrigerador',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'delayed': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'humedal_delayed',
        'USER': 'postgres',
        'PASSWORD': 'refrigerador',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
}
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Ajuste de zona horaria a Chile
TIME_ZONE = 'America/Santiago'  
USE_TZ = True  
USE_I18N = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Si esta en desarrollo, usar esta configuración para que Django sirva archivos estáticos.
if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / "static",  # Esto incluye la carpeta 'static' dentro del proyecto
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ruta para guardar los archivos
 
import os

# Ruta de los archivos de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Directorio donde se guardara el archivo de respaldo
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')  # Carpeta en el servidor para respaldo
