from django.urls import path

from .views import (
    GroupView,
)

urlpatterns = [
    path(
        route='group/<uuid:group_id>/',
        view=GroupView.as_view(),
    ),
]
