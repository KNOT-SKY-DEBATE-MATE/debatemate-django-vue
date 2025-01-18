from django.urls import path
from channels.routing import URLRouter

from .consumers import (
    MeetingMessageConsumer
)