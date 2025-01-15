from django.urls import path

from .api_views import (
    DiscussionAPIView,
    DiscussionOneAPIView,
    DiscussionMemberAPIView,
    DiscussionMemberOneAPIView,
    DiscussionMessageAPIView,
    DiscussionMessageOneAPIView,
    DiscussionMessageAnnotationAPIView,
)

urlpatterns = [

    # For discussion table
    path(
        route='group/<uuid:group_id>/discussion/',
        view=DiscussionAPIView.as_view(),
    ),

    # For one discussion
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/',
        view=DiscussionOneAPIView.as_view(),
    ),

    # For discussion member
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/member/',
        view=DiscussionMemberAPIView.as_view(),
    ),

    # For one discussion member
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/member/<int:member_id>/',
        view=DiscussionMemberOneAPIView.as_view(),
    ),

    # For discussion message
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/message/',
        view=DiscussionMessageAPIView.as_view(),
    ),

    # For one discussion message
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/message/<int:message_id>/',
        view=DiscussionMessageOneAPIView.as_view(),
    ),

    # For discussion message announce
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/message/<int:message_id>/annotation/',
        view=DiscussionMessageAnnotationAPIView.as_view(),
    ),
]
