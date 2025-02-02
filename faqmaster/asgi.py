"""
ASGI config for faqmaster project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faqmaster.settings')

application = get_asgi_application()
