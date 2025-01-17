from django.urls import path

from .api_views import (
    UserCSRFTokenAPIView,
    UserSignupAPIView,
    UserSigninAPIView,
    UserSignoutAPIView,
    UserOneAPIView,
    UserGroupAPIView,
)

urlpatterns = [
    path(
        route='csrftoken/',
        view=UserCSRFTokenAPIView.as_view(),
        name='api.user.csrftoken',
    ),
    path(
        route='signup/',
        view=UserSignupAPIView.as_view(),
        name='api.user.signup',
    ),
    path(
        route='signin/',
        view=UserSigninAPIView.as_view(),
        name='api.user.signin',
    ),
    path(
        route='signout/',
        view=UserSignoutAPIView.as_view(),
        name='api.user.signout',
    ),
    path(
        route='<int:user_id>/',
        view=UserOneAPIView.as_view(),
        name='api.user.(id)',
    ),
    path(
        route='<int:user_id>/group/',
        view=UserGroupAPIView.as_view(),
    ),
]
