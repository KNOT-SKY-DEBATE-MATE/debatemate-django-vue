import uuid

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

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


@method_decorator(csrf_exempt, name='dispatch')
class UserSigninAPIView(APIView):

    """
    View for user signin
    """

    class PostInSerializer(serializers.Serializer):

        # Define serializer
        username = serializers.CharField(max_length=255, required=True)

        # Define serializer
        password = serializers.CharField(max_length=255, required=True)

    def post(self, request: Request):

        # Get data from request
        serializer = self.PostInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save user
        user = authenticate(request=request, **serializer.validated_data)

        # Check if user exists
        if user is None:
            return Response(status=401)

        # Login user
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

        # Check if user exists
        user = User.objects.create_user(**serializer.validated_data)

        # Login user
        login(request, user)

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
        return Response(status=201)


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
