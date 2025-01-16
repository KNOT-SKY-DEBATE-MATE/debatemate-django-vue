from django.urls import path

from .views import (
    MeetingView,
)

urlpatterns = [

    # For meeting
    path(
        route='group/<uuid:group_id>/meeting/<uuid:meeting_id>/',
        view=MeetingView.as_view(),
    ),
]
