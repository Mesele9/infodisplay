import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from display.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infodisplay.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ws_urlpatterns
        )
    ),
})
