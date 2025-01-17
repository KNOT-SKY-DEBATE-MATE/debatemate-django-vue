from django.urls import path, include

from .views import (
    UserAuthenticationView,
    UserView,
)

urlpatterns = [
    path(
        route='authentication/',
        view=UserAuthenticationView.as_view(),
        name='user.authentication',
    ),
    path(
        route='',
        view=UserView.as_view(),
        name='user',
    ),
    path(
        route='oauth2/',
        view=include('allauth.urls'),
    ),
]
