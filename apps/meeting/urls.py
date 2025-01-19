# apps/meeting/urls.py
from django.urls import path
from .views import MeetingView, UserListView

from .views import (
    MeetingView,
)

urlpatterns = [
    path(
        route='<uuid:meeting_id>/',
        view=MeetingView.as_view(),
        name='meeting.(id)',
    ),
    path(
        route='userlist/<uuid:meeting_id>/',
        view=UserListView.as_view(), 
        name='meeting-userlist'
        ),
]