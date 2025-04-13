import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve().parent.parent.parent
files_and_dirs = os.listdir(BASE_DIR)

load_dotenv(BASE_DIR / '.env')
SECRET_KEY = os.getenv('SECRET_KEY')
VERSION = os.getenv('VERSION')
NOMAD_TOKEN = os.getenv('NOMAD_TOKEN')
CRM_TOKEN = f"Bearer {NOMAD_TOKEN}"
API_KEY_GOOGLE = os.getenv('GOOGLE_TOKEN')
HOME_HOST = os.getenv('HOME_HOST')

if VERSION == 'deploy':
    DEBUG = True
    ALLOWED_HOSTS = [HOME_HOST,f'www.{HOME_HOST}']
    CSRF_TRUSTED_ORIGINS = [f'https://{HOME_HOST}', f'https://{HOME_HOST}']
    HOST_PREFIX = f'https://{HOME_HOST}'
elif VERSION == 'development':
    DEBUG = True
    HOST_PREFIX = ''
else:
    raise ValueError('VERSION can be either DEV or DEPLOY')

WSGI_APPLICATION = 'stations.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'api_backend.apps.ApiBackendConfig',
    'clients.apps.ClientsConfig',
    'shop.apps.ShopConfig',
    'crm.apps.CrmConfig',
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

ROOT_URLCONF = 'stations.urls'

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

WSGI_APPLICATION = 'stations.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),

    }
}



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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if VERSION == 'deploy':
    FORCE_SCRIPT_NAME = '/water/'
    BASE_URL = '/water'
    MEDIA_URL = BASE_URL + '/media/'
    STATIC_URL =BASE_URL + '/static/'
elif VERSION == 'development':
    MEDIA_URL = '/media/'
    STATIC_URL = '/static/'
else:
    raise ValueError('VERSION can be either development or deploy')

STATIC_ROOT =  '/var/www/static'
MEDIA_ROOT = '/var/www/media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

TIME_ZONE = 'Asia/Almaty'
USE_TZ = True
LANGUAGE_CODE= 'ru-ru'



CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # важно!
    'formatters': {
        'simple': {
            'format': '[{asctime}] [{levelname}] [{name}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'Views| Summon': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
    }