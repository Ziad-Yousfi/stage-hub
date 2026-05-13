"""
ASGI config for the internship management platform.
Supports WebSocket connections for real-time notifications.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = get_asgi_application()
