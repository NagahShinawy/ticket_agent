"""
WSGI config for ticket_agent project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

env = config('DJANGO_ENV', default='dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'ticket_agent.settings.{env}')

application = get_wsgi_application()
