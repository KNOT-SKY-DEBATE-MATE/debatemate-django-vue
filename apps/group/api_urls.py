from django.urls import path

from .api_views import (
    GroupAPIView,
    GroupOneAPIView,
    GroupMemberAPIView,
    GroupMemberOneAPIView,
    GroupMemberInvitableAPIView,
    GroupMessageAPIView,
    GroupMessageOneAPIView,
)

urlpatterns = [
    path(
        route='api/group/',
        view=GroupAPIView.as_view(),
        name='api.group',
    ),
    path(
        route='api/group/<uuid:group_id>/',
        view=GroupOneAPIView.as_view(),
        name='api.group.(id)',
    ),
    path(
        route='api/group/<uuid:group_id>/member/',
        view=GroupMemberAPIView.as_view(),
        name='api.group.(id).member',
    ),
    path(
        route='api/group/<uuid:group_id>/member/<int:member_id>/',
        view=GroupMemberOneAPIView.as_view(),
        name='api.group.(id).member.(id)',
    ),
    path(
        route='api/group/<uuid:group_id>/member/invitable/',
        view=GroupMemberInvitableAPIView.as_view(),
        name='api.group.(id).member.invitable',
    ),
    path(
        route='api/group/<uuid:group_id>/message/',
        view=GroupMessageAPIView.as_view(),
        name='api.group.(id).message',
    ),
    path(
        route='api/group/<uuid:group_id>/message/<int:message_id>/',
        view=GroupMessageOneAPIView.as_view(),
        name='api.group.(id).message.(id)',
    ),
]
