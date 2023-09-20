from django.urls import path

from .consumers import DisplayConsumer

ws_urlpatterns = [
    path('ws/display', DisplayConsumer.as_asgi())
]