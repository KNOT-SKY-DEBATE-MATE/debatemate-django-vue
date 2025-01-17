# apps/meeting/urls.py
from .views import MeetingView
from django.urls import path
from .api_views import (
    MeetingAPIView,
    MeetingOneAPIView,
    MeetingMemberAPIView,
    MeetingMessageAPIView
)

urlpatterns = [
    path('api/group/<uuid:group_id>/meeting/',
         MeetingAPIView.as_view(),
         name='meeting-list'),
         
    path('api/group/<uuid:group_id>/meeting/<uuid:meeting_id>/',
         MeetingOneAPIView.as_view(),
        name='group.(id).meeting.(id)',
         name='meeting-detail'),
         
    path('api/group/<uuid:group_id>/meeting/<uuid:meeting_id>/member/',
         MeetingMemberAPIView.as_view(),
         name='meeting-member-list'),
         
    path('api/group/<uuid:group_id>/meeting/<uuid:meeting_id>/message/',
         MeetingMessageAPIView.as_view(),
         name='meeting-message-list'),
]