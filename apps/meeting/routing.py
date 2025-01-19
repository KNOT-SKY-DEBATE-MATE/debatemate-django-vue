# apps/meeting/routing.py
from django.urls import path
from channels.routing import URLRouter

from .consumers import (
    MeetingMessageConsumer
)

websocket_urlpatterns = urlpatterns = [
    path(
        route='ws/meeting/<uuid:meeting_id>/message/',
        view=MeetingMessageConsumer.as_asgi(),
    ),
]