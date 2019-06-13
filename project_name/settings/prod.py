from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost',]


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DEFAULT_DATABASE_NAME'),
        'USER': os.environ.get('DEFAULT_DATABASE_USER'),
        'PASSWORD': os.environ.get('DEFAULT_DATABASE_PASSWORD'),
        'HOST': os.environ.get('DEFAULT_DATABASE_HOST'),
        'PORT': os.environ.get('DEFAULT_DATABASE_PORT'),
    }
}