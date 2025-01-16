from django.urls import path

from .api_views import (
    MeetingAPIView,
    MeetingOneAPIView,
    MeetingMemberAPIView,
    MeetingMemberOneAPIView,
    MeetingMessageAPIView,
    MeetingMessageOneAPIView,
    MeetingMessageAnnotationAPIView,
)

urlpatterns = [
    path(
        route='group/<uuid:group_id>/meeting/',
        view=MeetingAPIView.as_view(),
    ),
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/',
        view=MeetingOneAPIView.as_view(),
    ),
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/member/',
        view=MeetingMemberAPIView.as_view(),
    ),
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/member/<int:member_id>/',
        view=MeetingMemberOneAPIView.as_view(),
    ),
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/message/',
        view=MeetingMessageAPIView.as_view(),
    ),
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/message/<int:message_id>/',
        view=MeetingMessageOneAPIView.as_view(),
    ),
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/message/<int:message_id>/annotation/',
        view=MeetingMessageAnnotationAPIView.as_view(),
    ),
]