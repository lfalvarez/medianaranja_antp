"""
Django settings for medianaranja_web project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IS_OFFLINE = os.environ.get('LAMBDA_TASK_ROOT') is None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(%oxpv3#3wg^z3@+-8t7s)@gp7ro0)-x*)^vq^5((l_n_5c_ui'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IS_OFFLINE

ALLOWED_HOSTS = ['k8936tfdt5.execute-api.sa-east-1.amazonaws.com',
                 'localhost',
                 'zappa',
                 'mn.felipe.al',
                 '127.0.0.1',
                 'participamostodxs.ahoranostocaparticipar.cl'
                 ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dj_proposals_candidates',
    'django_s3_storage',
    'mn_juego',
]
if IS_OFFLINE:
    INSTALLED_APPS += ['django_extensions']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medianaranja_web.urls'

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

WSGI_APPLICATION = 'medianaranja_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if IS_OFFLINE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / "sqlite.db"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django_s3_sqlite",
            "NAME": "sqlite.db",
            "BUCKET": "medianaranja-antp",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

BALDINHO = "antp-assets"

# STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"





AWS_S3_BUCKET_NAME_STATIC = BALDINHO

# These next two lines will serve the static files directly
# from the s3 bucket
DOMINIO_PERSONALIZADO = '%s.s3.amazonaws.com' % BALDINHO
AWS_DEFAULT_ACL = None

if not IS_OFFLINE:
    STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    STATIC_URL = "https://%s/" % DOMINIO_PERSONALIZADO
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR

# Ids de cosas para hacerle_referencia
GEP_PROPOSAL_REMOTE_ID = 8  # El id que tiene la propuesta GEP en decidim
PARTICIPACION_PROPOSAL_REMOTE_ID = 7  # el id que tiene la propuesta por la participacion en decidim
COUNTRY_ID = 1  # el id de chile, territorio al cual estaran asociadas las propuestas de arriba



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
#past the key or password app here
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
A_QUIEN_SE_LE_VA_ELMAIL = os.environ['A_QUIEN_SE_LE_VA_ELMAIL']