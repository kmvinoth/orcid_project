from .base import *

DEBUG = False

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# INTERNAL_IPS = ('127.0.0.1',)  # for django-debug-toolbar
