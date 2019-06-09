import os
from .base import *

DEBUG = True
CORS_ORIGIN_ALLOW_ALL = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
