from django.urls import path
from channels.routing import URLRouter

from .consumers import (
    GroupMessageConsumer
)

websocket_urlpatterns = urlpatterns = [
    path(
        route='ws/group/<uuid:group_id>/message/',
        view=GroupMessageConsumer.as_asgi(),
    ),
]
