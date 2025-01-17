# apps/meeting/api_views.py
import requests
import uuid

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

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

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        # Get group
        meetings = Meeting.objects.all()

        # Validate data
        serializer = MeetingSerializer(meetings, many=True)

        # Return group
        return Response(serializer.data)

    def post(self, request: Request):

        # Get data from request
        serializer = MeetingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save meeting
        meeting = serializer.save()

        # Add first user to group
        group_member = get_object_or_404(GroupMember, user=request.user, group=meeting.group)

        # Return group
        MeetingMember.objects.create(meeting=meeting, member=group_member, is_admin=True, nickname=group_member.nickname)

        # Validate data
        return Response(serializer.data)


class MeetingOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any meeting
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user)\
                .exists():
            return Response(status=403)

        # Validate data
        serializer = MeetingSerializer(meeting)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = MeetingSerializer(meeting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class MeetingMemberAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting members
        meeting_members = MeetingMember.objects.filter(meeting=meeting)

        # Validate data
        serializer = MeetingMemberSerializer(meeting_members, many=True)

        # Return meeting
        return Response(serializer.data)

    def post(self, request: Request, meeting_id):

        # グループ取得
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # 管理者権限チェック
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user, is_admin=True)\
                .exists():
            return Response(status=403)

        # メンバー追加処理
        serializer = MeetingMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(meeting=meeting)

        # Validate data
        return Response(serializer.data)


class MeetingMemberOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id, member_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting member
        meeting_member = get_object_or_404(MeetingMember, id=member_id, meeting=meeting)

        # Validate data
        serializer = MeetingMemberSerializer(meeting_member)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, meeting_id, member_id):

        # Get group
        meeting = get_object_or_404(Meeting, id=meeting_id)

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

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting messages
        meeting_messages = MeetingMessage.objects.filter(meeting=meeting)

        # Validate data
        serializer = MeetingMessageSerializer(meeting_messages, many=True)

        # Return meeting
        return Response(serializer.data)

    def post(self, request: Request, meeting_id):

        # Get group
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Get meeting member
        meeting_member = get_object_or_404(MeetingMember, meeting=meeting, member=request.user)

        # Get data from request
        serializer = MeetingMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=meeting_member, meeting=meeting)

        # Validate data
        return Response(serializer.data)


class MeetingMessageOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id, message_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        # Validate data
        serializer = MeetingMessageSerializer(meeting_message)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, meeting_id, message_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Get meeting message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        # Get data from request
        serializer = MeetingMessageSerializer(meeting_message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class MeetingMessageAnnotationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id, message_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not MeetingMember.objects\
                .filter(meeting=meeting, member__user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting-message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        try:
            # Get meeting-message
            meeting_message_annotation = MeetingMessageAnnotation.objects\
                .get(meeting=meeting, message_id=message_id)
            
            # Get meeting-messages
            serializer = MeetingMessageAnnotationSerializer(meeting_message_annotation)
        
        except MeetingMessageAnnotation.DoesNotExist:
            
            # Get meeting
            serializer = MeetingMessageSerializer(meeting_message)

            try:
                # Get meeting-messages
                response = requests.post("...", json=serializer.data)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:

                # Return meeting
                return Response(status=err.response.status_code)
            
            # Validate data
            serializer = MeetingMessageAnnotationSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            serializer.save(message=meeting_message, meeting=meeting)

        # Return meeting
        return Response(serializer.data)
