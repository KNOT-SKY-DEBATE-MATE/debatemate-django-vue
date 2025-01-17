# apps/meeting/urls.py
from .views import MeetingView
from django.urls import path
from .views import (
    MeetingView,
)

urlpatterns = [
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/',
        view=MeetingView.as_view(),
        name='group.(id).meeting.(id)',
    ),
]