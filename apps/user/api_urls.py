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
        route='api/user/csrftoken/',
        view=UserCSRFTokenAPIView.as_view(),
    ),
    path(
        route='api/user/signup/',
        view=UserSignupAPIView.as_view(),
    ),
    path(
        route='api/user/signin/',
        view=UserSigninAPIView.as_view(),
    ),
    path(
        route='api/user/signout/',
        view=UserSignoutAPIView.as_view(),
    ),
    path(
        route='api/user/<int:user_id>/',
        view=UserOneAPIView.as_view(),
    ),
    path(
        route='api/user/<int:user_id>/group/',
        view=UserGroupAPIView.as_view(),
    ),
]
