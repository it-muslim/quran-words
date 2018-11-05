import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

WSGI_APPLICATION = 'config.wsgi.application'
