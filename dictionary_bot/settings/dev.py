from .base import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-+_rvd_sjsyd408rt6%0&5#^)tx@6sdiyen)fi1q4!m%yz33y&-'

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS += [
    "debug_toolbar"
]

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
