from .base import *
from decouple import config

DEBUG = True

INSTALLED_APPS += ['debug_toolbar',  ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

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

INTERNAL_IPS = ('127.0.0.1',)  # for django-debug-toolbar

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = ["/mnt/u/s-it/orcid_project/public_api/static/public_api/"]

if DEBUG:
    # Charite Email settings (working)
    # EMAIL_HOST = 'exchange-smtp.charite.de'
    # EMAIL_PORT = 587
    # EMAIL_HOST_USER = config('CHARITE_USER')
    # EMAIL_HOST_PASSWORD = config('CHARITE_PASSWORD')
    # EMAIL_USE_TLS = True

    # Local SMTP SERVER
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'testing@example.com'