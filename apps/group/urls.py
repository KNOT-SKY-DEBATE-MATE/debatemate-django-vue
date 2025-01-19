from django.urls import re_path

from .views import (
    GroupView,
)

urlpatterns = [
    re_path(
        r'^(?P<group_id>[0-9a-fA-F]{32})/$',
        GroupView.as_view(),
    ),
]
