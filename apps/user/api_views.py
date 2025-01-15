import uuid

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    User
)

from .serializers import (
    UserSerializer
)

from apps.group.models import (
    Group
)

from apps.group.serializers import (
    GroupSerializer
)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserCSRFTokenAPIView(APIView):

    """
    View for csrf cookie
    """

    def get(self, request: Request):

        # Return csrf cookie
        return Response(status=200)


class UserSigninAPIView(APIView):

    """
    View for user signin
    """

    def post(self, request: Request):

        # Get data from request
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        data = serializer.validated_data

        # Save user
        user = authenticate(request=request, username=data['username'], password=data['password'])

        # Check if user exists
        if user is None:
            return Response(status=401)

        # Login user
        if not user.is_authenticated:
            logout(request)

        login(request, user)

        # Return token
        return Response(status=201)


class UserSignupAPIView(APIView):

    """
    View for user signup
    """

    def post(self, request: Request):

        # Get data from request
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        data = serializer.validated_data

        # Check if user exists
        if User.objects.filter(username=data['username']).exists():
            return Response(status=401)

        # Save user
        user = User(username=data['username'])
        user.set_password(raw_password=data['password'])
        user.save()

        # Login user
        login(request, user)

        # Validate data
        serializer = UserSerializer(user)

        # Return token
        return Response(status=201)


class UserSignoutAPIView(APIView):

    """
    View for user signout
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request):

        # Logout user
        logout(request)

        # Return response
        return Response(status=200)


class UserOneAPIView(APIView):

    """
    View for user one
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, user_id: uuid.UUID):

        # Get user
        user = get_object_or_404(User, id=user_id)

        # Validate data
        serializer = UserSerializer(user)

        # Return user
        return Response(serializer.data)


class UserGroupAPIView(APIView):

    """
    View for user group
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, user_id: uuid.UUID):

        # Get user
        user = get_object_or_404(User, id=user_id)

        # Check if user is a member of any group
        if user != request.user:
            return Response(status=403)

        # Get user-groups
        groups = Group.objects.filter(groupmember__user=user)

        # Validate data
        serializer = GroupSerializer(groups, many=True)

        # Return groups
        return Response(serializer.data)
