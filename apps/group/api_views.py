import requests

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
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

from apps.meeting.models import (
    Meeting
)

from apps.meeting.serializers import (
    MeetingSerializer
)

from apps.user.serializers import (
    UserSerializer
)


class GroupAPIView(APIView):

    """
    View for group.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(GroupSerializer):
        pass

    def get(self, request: Request):

        # Get group
        groups = Group.objects.filter(groupmember__user=request.user)

        # Validate data
        serializer = self.GetOutSerializer(groups, many=True)

        # Return groups
        return Response(serializer.data)

    class PostSerializer(GroupSerializer):
        pass

    class PostOutSerializer(GroupSerializer):

        # Serializer settings
        class Meta(GroupSerializer.Meta):
            depth = 1

    def post(self, request: Request):

        # Get group
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Transaction for group and group-member
        with transaction.atomic():

            # Save group
            group = serializer.save()

            # Add first user to group
            GroupMember.objects\
                .create(group=group, user=request.user, nickname=request.user.username, is_admin=True)

        # Validate data
        out_serializer = self.PostOutSerializer(group)

        # Return group
        return Response(out_serializer.data)


class GroupOneAPIView(APIView):

    """
    View for group.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(GroupSerializer):

        # Serializer settings
        class Meta(GroupSerializer.Meta):
            depth = 1

    def get(self, request: Request, group_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Validate data
        out_serializer = self.GetOutSerializer(group)

        # Return group
        return Response(out_serializer.data)

    class PatchSerializer(GroupSerializer):

        # Serializer settings
        class Meta(GroupSerializer.Meta):
            fields = ['name', 'description']

    class PatchOutSerializer(GroupSerializer):

        # Serializer settings
        class Meta(GroupSerializer.Meta):
            depth = 1

    def patch(self, request: Request, group_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = self.PatchOutSerializer(
            group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save
        group_member = serializer.save()

        # Validate data
        out_serializer = self.PatchOutSerializer(group_member)

        try:
            # Post event to websocket server
            response = requests.post(
                settings.WEBSOCKET_URL + f'on/group/{group.id}/update/')
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass

        # Return group
        return Response(out_serializer.data)


class GroupMemberAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(GroupMemberSerializer):

        # Serializer settings
        class Meta(GroupMemberSerializer.Meta):
            depth = 1

    def get(self, request: Request, group_id):

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
        out_serializer = self.GetOutSerializer(group_members, many=True)

        # Return group
        return Response(out_serializer.data)

    class PostSerializer(GroupMemberSerializer):

        # Serializer settings
        class Meta(GroupMemberSerializer.Meta):
            fields = ['user', 'nickname']

    class PostOutSerializer(GroupMemberSerializer):

        # Serializer settings
        class Meta(GroupMemberSerializer.Meta):
            depth = 1

    def post(self, request: Request, group_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save and get group-member
        group_member = serializer.save(group=group)

        # Validate data
        out_serializer = self.PostOutSerializer(group_member)

        # Post event to websocket server
        try:
            response = requests.post(
                settings.WEBSOCKET_URL + f'on/group/{group.id}/member.invite/')
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass

        # Return group
        return Response(out_serializer.data)


class GroupMemberOneAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(GroupMemberSerializer):

        # Serializer settings
        class Meta(GroupMemberSerializer.Meta):
            depth = 1

    def get(self, request: Request, group_id, member_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_member = get_object_or_404(
            GroupMember, id=member_id, group=group)

        # Validate data
        out_serializer = self.GetOutSerializer(group_member)

        # Return group
        return Response(out_serializer.data)

    class PatchSerializer(GroupMemberSerializer):

        # Serializer settings
        class Meta(GroupMemberSerializer.Meta):
            fields = ['nickname']

    class PatchOutSerializer(GroupMemberSerializer):

        # Serializer settings
        class Meta(GroupMemberSerializer.Meta):
            depth = 1

    def patch(self, request: Request, group_id, member_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_member = get_object_or_404(
            GroupMember, id=member_id, group=group)

        # Get data from request
        serializer = self.PatchSerializer(
            group_member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save and get group-member
        group_member = serializer.save()

        # Validate data
        out_serializer = self.PatchOutSerializer(group_member)

        # Post event to websocket server
        try:
            response = requests.post(
                settings.WEBSOCKET_URL + f'on/group/{group.id}/member.update/')
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass

        # Return group
        return Response(out_serializer.data)


class GroupMemberInvitableAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(UserSerializer):
        
        # Serializer settings
        class Meta(UserSerializer.Meta):
            fields = ['id', 'username']

    def get(self, request: Request, group_id):

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
        out_serializer = self.GetOutSerializer(users, many=True)

        # Return group
        return Response(out_serializer.data)


class GroupMessageAPIView(APIView):

    """
    View for group message.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(GroupMessageSerializer):

        # Serializer settings
        class Meta(GroupMessageSerializer.Meta):
            depth = 1

    def get(self, request: Request, group_id):

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
        out_serializer = self.GetOutSerializer(group_messages, many=True)

        # Return group
        return Response(out_serializer.data)

    class PostSerializer(GroupMessageSerializer):

        # Serializer settings
        class Meta(GroupMessageSerializer.Meta):
            fields = ['content']

    class PostOutSerializer(GroupMessageSerializer):

        # Serializer meta properties
        class Meta(GroupMessageSerializer.Meta):
            depth = 1

    def post(self, request: Request, group_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Get group-member
        group_member = get_object_or_404(
            GroupMember, group=group, user=request.user)

        # Get data from request
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save group-message
        group_message = serializer.save(group=group, sender=group_member)

        # Post event
        try:
            # Post event to websocket server
            response = requests.post(
                settings.WEBSOCKET_URL + f'on/group/{group.id}/message.create/')
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass

        # Validate data
        out_serializer = self.PostOutSerializer(group_message)

        # Return group
        return Response(out_serializer.data)


class GroupMessageOneAPIView(APIView):

    """
    View for group message.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(GroupMessageSerializer):

        # Serializer settings
        class Meta(GroupMessageSerializer.Meta):
            depth = 1

    def get(self, request: Request, group_id, message_id):

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
        out_serializer = self.GetOutSerializer(group_message)

        # Return group
        return Response(out_serializer.data)

    class PatchSerializer(GroupMessageSerializer):

        # Serializer settings
        class Meta(GroupMessageSerializer.Meta):
            fields = ['content']

    class PatchOutSerializer(GroupMessageSerializer):

        # Serializer meta properties
        class Meta(GroupMessageSerializer.Meta):
            depth = 1

    def patch(self, request: Request, group_id, message_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Check if user is a member of any group
        group_message = get_object_or_404(
            GroupMessage, id=message_id, group=group)

        # Get data from request
        serializer = self.PatchSerializer(group_message, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save group-message
        group_message = serializer.save()

        # Validate data
        out_serializer = self.PatchOutSerializer(group_message)

        # Get channel layer
        return Response(out_serializer.data)


class GroupMeetingAPIView(APIView):

    """
    View for group meeting.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingSerializer):

        # Serializer settings
        class Meta(MeetingSerializer.Meta):
            depth = 1

    def get(self, request: Request, group_id):

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
        serializer = self.GetOutSerializer(meeting, many=True)

        # Return group
        return Response(serializer.data)
