from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

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

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
