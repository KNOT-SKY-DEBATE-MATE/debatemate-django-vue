from django.urls import path, include

from .views import (
    UserAuthenticationView,
    UserView,
)

urlpatterns = [
    path(
        route='user/authentication/',
        view=UserAuthenticationView.as_view(),
        name='user.authentication',
    ),
    path(
        route='user/',
        view=UserView.as_view(),
        name='user',
    ),
    path(
        route='user/login/',
        view=include('allauth.urls'),
        name='user.login',
    )
]
