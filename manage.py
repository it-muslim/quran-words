#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

if __name__ == '__main__':
    DJANGO_EXECUTION_ENVIRONMENT = os.getenv(
        "DJANGO_EXECUTION_ENVIRONMENT", "DEVELOPMENT")
    if DJANGO_EXECUTION_ENVIRONMENT == "DEVELOPMENT":
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "config.settings.development")
    elif DJANGO_EXECUTION_ENVIRONMENT == "PRODUCTION":
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "config.settings.production")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
