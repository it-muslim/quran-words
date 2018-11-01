import os

DEBUG = False

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') \
    if os.getenv('ALLOWED_HOSTS') else None
