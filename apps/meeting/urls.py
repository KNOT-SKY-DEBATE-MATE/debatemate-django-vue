# apps/meeting/urls.py

from django.urls import path
from .views import (
    MeetingView,
    MeetingListView,  # DiscussionListView から変更
    MeetingDetailView,  # DiscussionDetailView から変更
)

urlpatterns = [
    # 既存のパス
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/',
        view=MeetingView.as_view(),
        name='group.(id).meeting.(id)',
    ),
    
    # 追加するパス
    path(
        route='api/group/<uuid:group_id>/meeting/',
        view=MeetingListView.as_view(),
        name='meeting-list'
    ),
    path(
        route='api/group/<uuid:group_id>/meeting/<uuid:meeting_id>/',
        view=MeetingDetailView.as_view(),
        name='meeting-detail'
    ),
]