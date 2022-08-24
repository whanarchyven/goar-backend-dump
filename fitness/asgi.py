"""
ASGI config for fitness project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitness.settings")
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat import routing
from chat.middleware import QueryAuthMiddleware


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": QueryAuthMiddleware(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
