from django.urls import path

from .views import (
    UserAuthenticationView,
    UserView,
)

urlpatterns = [
    path(
        route='user/authentication/',
        view=UserAuthenticationView.as_view(),
    ),
    path(
        route='user/',
        view=UserView.as_view(),
    ),
]
