import requests
import bleach
import uuid

from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


from apps.group.models import (
    Group,
    GroupMember,
)

from apps.group.serializers import (
    GroupSerializer,
    GroupMemberSerializer,
)


from .models import (
    Discussion,
    DiscussionMember,
    DiscussionMessage,
    DiscussionMessageAnnotation,
)

from .serializers import (
    DiscussionSerializer,
    DiscussionMemberSerializer,
    DiscussionMessageSerializer,
    DiscussionMessageAnnotationSerializer,
)


class DiscussionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get group members
        discusssions =\
            Discussion.objects.filter(group=group)

        # Validate data
        serializer = DiscussionSerializer(discusssions, many=True)

        # Return group
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID):

        # Get group id
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get group
        serializer = DiscussionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(group=group)

        # Return discussion
        return Response(serializer.data)


class DiscussionOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion = get_object_or_404(
            Discussion, id=discussion_id, group=group)

        # Validate data
        serializer = DiscussionSerializer(discussion)

        # Return discussion
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion = get_object_or_404(
            Discussion, id=discussion_id, group=group)

        # Get data from request
        serializer = DiscussionSerializer(
            discussion, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class DiscussionMemberAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get discussion members
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get discussion members
        discussion_members =\
            DiscussionMember.objects.filter(discussion=discussion)

        # Validate data
        serializer = DiscussionMemberSerializer(discussion_members, many=True)

        # Return discussion
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion = get_object_or_404(
            Discussion, id=discussion_id, group=group)

        # Get data from request
        serializer = DiscussionMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(discussion=discussion)

        # Return discussion
        return Response(serializer.data)


class DiscussionMemberOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID, member_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get discussion member
        discussion_member =\
            get_object_or_404(DiscussionMember, id=member_id, discussion=discussion)

        # Validate data
        serializer = DiscussionMemberSerializer(discussion_member)

        # Return discussion
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID, member_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get discussion member
        discussion_member =\
            get_object_or_404(DiscussionMember, id=member_id, discussion=discussion)

        # Get data from request
        serializer = DiscussionMemberSerializer(discussion_member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class DiscussionMessageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get discussion messages
        discussion_messages =\
            DiscussionMessage.objects.filter(discussion=discussion)

        # Validate data
        serializer = DiscussionMessageSerializer(discussion_messages, many=True)

        # Return discussion
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get data from request
        serializer = DiscussionMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(discussion=discussion)

        # Return discussion
        return Response(serializer.data)


class DiscussionMessageOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID, message_id: uuid.UUID):
        
        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get discussion message
        discussion_message =\
            get_object_or_404(DiscussionMessage, id=message_id, discussion=discussion)

        # Validate data
        serializer = DiscussionMessageSerializer(discussion_message)

        # Return discussion
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID, message_id: uuid.UUID):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)
        
        # Get discussion message
        discussion_message =\
            get_object_or_404(DiscussionMessage, id=message_id, discussion=discussion)

        # Get data from request
        serializer = DiscussionMessageSerializer(discussion_message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class DiscussionMessageAnnotationAPIView(APIView):

    def get(self, request: Request, group_id: uuid.UUID, discussion_id: uuid.UUID, message_id: int):

        # Get discussion
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)
        
        # Get discussion
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Get discussion message
        discussion_message =\
            get_object_or_404(DiscussionMessage, id=message_id, discussion=discussion)
        
        try:
            # Get discussion message
            discussion_message_annotation =\
                DiscussionMessageAnnotation.objects.get(discussion=discussion, message_id=message_id)
            # Get discussion messages
            serializer = DiscussionMessageAnnotationSerializer(discussion_message_annotation)
        except DiscussionMessageAnnotation.DoesNotExist:
            # Get discussion messages
            serializer = DiscussionMessageSerializer(discussion_message)
            # Send request
            try:
                response = requests.post("dummy.com/dummy", json=serializer.data)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                return Response(err)
            # Return discussion
            serializer = DiscussionMessageAnnotationSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            serializer.save(message=discussion_message, discussion=discussion)

        # Return discussion
        return Response(serializer.data)
