"""
ASGI config for ticket_agent project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from decouple import config
from django.core.asgi import get_asgi_application

env = config('DJANGO_ENV', default='dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'ticket_agent.settings.{env}')

application = get_asgi_application()
