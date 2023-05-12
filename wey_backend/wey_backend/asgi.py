"""
ASGI config for tryToDjangoChannels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from chat.consumers import MyConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wey_backend.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # Not work with uuid
            re_path(r'ws/(?P<room_name>[A-Za-z0-9_-]+)/', MyConsumer.as_asgi())
        ])
    )
})
