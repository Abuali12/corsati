from .settings import *
from .settings import BASE_DIR
from pathlib import Path
import os

import dj_database_url

# Database
DATABASES= {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',



    'allauth.account.middleware.AccountMiddleware',
]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE= 'whitenoise.storage.CompressedManifestStaticFilesStorage'
