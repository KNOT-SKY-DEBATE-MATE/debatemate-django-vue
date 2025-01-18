# apps/group/api_views.py
import uuid

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from .models import (
    Group,
    GroupMember,
    GroupMessage,
)

from .serializers import (
    GroupSerializer,
    GroupMemberSerializer,
    GroupMessageSerializer,
)

from apps.user.serializers import (
    UserSerializer
)

from apps.meeting.models import (
    Meeting
)

from apps.meeting.serializers import (
    MeetingPostSerializer
)


class GroupAPIView(APIView):

    """
    View for group.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        # Get group
        groups = Group.objects.all()

        # Validate data
        serializer = GroupSerializer(groups, many=True)

        # Return groups
        return Response(serializer.data)

    def post(self, request: Request):

        # Get group
        serializer = GroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save group
        group = serializer.save()

        # Add first user to group
        GroupMember.objects.create(user=request.user, group=group, is_admin=True, nickname=request.user.username)

        # Validate data
        serializer = GroupSerializer(group)

        # Return group
        return Response(serializer.data)


class GroupOneAPIView(APIView):

    """
    View for group.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Validate data
        serializer = GroupSerializer(group)

        # Return group
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = GroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class GroupMemberAPIView(APIView):

    """
    View for group member.
    """

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
        group_members = GroupMember.objects.filter(group=group)

        # Validate data
        serializer = GroupMemberSerializer(group_members, many=True)

        # Return group
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = GroupMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(group=group)

        # Validate data
        return Response(serializer.data)


class GroupMemberOneAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, member_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_member = get_object_or_404(GroupMember, id=member_id, group=group)

        # Validate data
        serializer = GroupMemberSerializer(group_member)

        # Return group
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, member_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_member = get_object_or_404(GroupMember, id=member_id, group=group)

        # Get data from request
        serializer = GroupMemberSerializer(group_member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class GroupMemberInvitableAPIView(APIView):

    """
    View for group member.
    """

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
        users = get_user_model().objects.exclude(groupmember__group=group)\
            .filter(username__icontains=request.query_params.get('query', ''))

        # Validate data
        serializer = UserSerializer(users, many=True)

        # Return group
        return Response(serializer.data)


class GroupMessageAPIView(APIView):

    """
    View for group message.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get group messages
        group_messages = GroupMessage.objects.filter(group=group)

        # Validate data
        serializer = GroupMessageSerializer(group_messages, many=True)

        # Return group
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Get group-member
        group_member = get_object_or_404(GroupMember, group=group, user=request.user)

        # Get data from request
        serializer = GroupMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=group_member, group=group)

        # Validate data
        return Response(serializer.data)


class GroupMessageOneAPIView(APIView):

    """
    View for group message.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, message_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_message = GroupMessage.objects.get(id=message_id, group=group)

        # Validate data
        serializer = GroupMessageSerializer(group_message)

        # Return group
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, message_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_message = get_object_or_404(GroupMessage, id=message_id, group=group)

        # Get data from request
        serializer = GroupMessageSerializer(group_message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class GroupMeetingAPIView(APIView):

    """
    View for group meeting.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get group-meetings
        meeting = Meeting.objects.filter(group=group)

        # Validate data
        serializer = MeetingPostSerializer(meeting, many=True)

        # Return group
        return Response(serializer.data)
