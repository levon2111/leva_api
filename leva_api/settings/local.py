# -*- coding: utf-8 -*-
from leva_api.settings.base import *

DEBUG = True
THUMBNAIL_DEBUG = True

BASE_URL = 'http://127.0.0.1:8000/'
CLIENT_BASE_URL = 'http://127.0.0.1:4200/'
ALLOWED_HOSTS = ['*', ]

BASE_PATH = "/var/www/leva_api/"

THIRD_PARTY_APPS += [
    'debug_toolbar',
    'django_extensions',
]

INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS + PROJECT_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'leva',
        'USER': 'leva_user',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
