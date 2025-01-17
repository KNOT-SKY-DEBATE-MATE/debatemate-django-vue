import requests
import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.group.models import (
    Group,
    GroupMember,
)

from .models import (
    Meeting,
    MeetingMember,
    MeetingMessage,
    MeetingMessageAnnotation,
)

from .serializers import (
    MeetingSerializer,
    MeetingMemberSerializer,
    MeetingMessageSerializer,
    MeetingMessageAnnotationSerializer,
)


class MeetingAPIView(APIView):

    """
    View for meeting.
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
        meetings = Meeting.objects.filter(group=group)

        # Validate data
        serializer = MeetingSerializer(meetings, many=True)

        # Return group
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID):

        # Get group id
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        group_member = get_object_or_404(GroupMember, group=group, user=request.user, is_admin=True)

        # Get group
        serializer = MeetingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(group=group)

        # Get group members
        MeetingMember.objects.create(meeting=serializer.instance, member=group_member, is_admin=True)

        # Return meeting
        return Response(serializer.data)


class MeetingOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Validate data
        serializer = MeetingSerializer(meeting)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get data from request
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class MeetingMemberAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting members
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting members
        meeting_members = MeetingMember.objects.filter(meeting=meeting)

        # Validate data
        serializer = MeetingMemberSerializer(meeting_members, many=True)

        # Return meeting
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get data from request
        serializer = MeetingMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(meeting=meeting)

        # Return meeting
        return Response(serializer.data)


class MeetingMemberOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID, member_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting member
        meeting_member = get_object_or_404(MeetingMember, id=member_id, meeting=meeting)

        # Validate data
        serializer = MeetingMemberSerializer(meeting_member)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID, member_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting member
        meeting_member = get_object_or_404(MeetingMember, id=member_id, meeting=meeting)

        # Get data from request
        serializer = MeetingMemberSerializer(meeting_member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class MeetingMessageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting messages
        meeting_messages = MeetingMessage.objects.filter(meeting=meeting)

        # Validate data
        serializer = MeetingMessageSerializer(meeting_messages, many=True)

        # Return meeting
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get data from request
        serializer = MeetingMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(meeting=meeting)

        # Return meeting
        return Response(serializer.data)


class MeetingMessageOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID, message_id: int):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        # Validate data
        serializer = MeetingMessageSerializer(meeting_message)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID, message_id: int):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        # Get data from request
        serializer = MeetingMessageSerializer(meeting_message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class MeetingMessageAnnotationAPIView(APIView):

    def get(self, request: Request, group_id: uuid.UUID, meeting_id: uuid.UUID, message_id: int):

        # Get meeting
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Get meeting message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        try:
            # Get meeting message
            meeting_message_annotation =\
                MeetingMessageAnnotation.objects.get(meeting=meeting, message_id=message_id)
            # Get meeting messages
            serializer = MeetingMessageAnnotationSerializer(meeting_message_annotation)
            # Return meeting
            return Response(serializer.data)
        except MeetingMessageAnnotation.DoesNotExist:
            # Get meeting messages
            serializer = MeetingMessageSerializer(meeting_message)
            # Send request
            try:
                response = requests.post("...", json=serializer.data)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                return Response(err)
            # Return meeting
            serializer = MeetingMessageAnnotationSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            serializer.save(message=meeting_message, meeting=meeting)
            # Return meeting
            return Response(serializer.data)
