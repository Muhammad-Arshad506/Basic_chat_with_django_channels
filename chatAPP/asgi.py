"""
ASGI config for chatAPP project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from chat.url import websocket_urlpatterns
from chat.ChannelsAuthMiddleware import TokenAuthMiddleWare
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatAPP.settings')

# application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket":TokenAuthMiddleWare(
            AllowedHostsOriginValidator(URLRouter(websocket_urlpatterns))
        )
    }
)