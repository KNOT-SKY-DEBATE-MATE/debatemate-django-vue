from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from .models import (
    Group,
    GroupMember,
    GroupMessage,
)

from apps.meeting.models import (
    Meeting
)


class GroupAPIView(APIView):

    """
    View for group.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = Group
            fields = ['id', 'name', 'description']

    def get(self, request: Request):

        # Get group
        groups = Group.objects.filter(groupmember__user=request.user)

        # Validate data
        serializer = self.GetOutSerializer(groups, many=True)

        # Return groups
        return Response(serializer.data)

    class PostSerializer(serializers.ModelSerializer):

        class Meta:
            model = Group
            fields = ['name', 'description']

    class PostOutSerializer(serializers.ModelSerializer):


        class Meta:
            model = Group
            fields = '__all__'

    def post(self, request: Request):

        # Get group
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Transaction for group and group-member
        with transaction.atomic():

            # Save group
            group = serializer.save()

            # Add first user to group
            group_member = GroupMember.objects\
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

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = Group
            fields = '__all__'

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

    class PatchSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = Group
            fields = ['name', 'description']

    class PatchOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = Group
            fields = '__all__'

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

        # Return group
        return Response(out_serializer.data)


class GroupMemberAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMember
            depth = 1
            fields = '__all__'

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

    class PostSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMember
            fields = ['user', 'nickname']

    class PostOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMember
            fields = '__all__'

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

        # Return group
        return Response(out_serializer.data)


class GroupMemberOneAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMember
            fields = '__all__'

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

    class PatchSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMember
            fields = ['nickname']

    class PatchOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMember
            fields = '__all__'

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

        # Return group
        return Response(out_serializer.data)


class GroupMemberInvitableAPIView(APIView):

    """
    View for group member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = get_user_model()
            fields = '__all__'

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

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMessage
            depth = 1
            fields = '__all__'

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

    class PostSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMessage
            fields = ['content']

    class PostOutSerializer(serializers.ModelSerializer):

        # Serializer meta properties
        class Meta:
            model = GroupMessage
            depth = 1
            fields = '__all__'

    def post(self, request: Request, group_id):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Get group-member
        group_member = get_object_or_404(GroupMember, group=group, user=request.user)

        # Get data from request
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save group-message
        group_message = serializer.save(group=group, sender=group_member)

        # Validate data
        out_serializer = self.PostOutSerializer(group_message)

        # Validate data
        return Response(out_serializer.data)


class GroupMessageOneAPIView(APIView):

    """
    View for group message.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMessage
            depth = 1
            fields = '__all__'

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

    class PatchSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = GroupMessage
            fields = ['content']

    class PatchOutSerializer(serializers.ModelSerializer):


        # Serializer meta properties
        class Meta:
            model = GroupMessage
            depth = 1
            fields = '__all__'

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

    class GetOutSerializer(serializers.ModelSerializer):

        # Serializer settings
        class Meta:
            model = Meeting
            depth = 2
            fields = '__all__'

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
