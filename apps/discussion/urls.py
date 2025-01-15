from django.urls import path

from .views import (
    DiscussionView,
)

urlpatterns = [

    # For discussion
    path(
        route='group/<uuid:group_id>/discussion/<uuid:discussion_id>/',
        view=DiscussionView.as_view(),
    ),
]
