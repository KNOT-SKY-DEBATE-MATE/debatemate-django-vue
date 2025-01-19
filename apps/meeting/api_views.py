# apps/meeting/api_views.py
import requests
import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers



from apps.group.models import (
    GroupMember,
)

from .models import (
    Meeting,
    MeetingMember,
    MeetingMessage,
    MeetingMessageAnnotation,

)

from .serializers import (

    MeetingPostSerializer,
    MeetingGetSerializer,
    MeetingMessageSerializer,
    MeetingMessageAnnotationSerializer,
)



class MeetingAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        # Get group
        meetings = Meeting.objects.all()

        # Validate data
        serializer = MeetingGetSerializer(meetings, many=True)

        # Return group
        return Response(serializer.data)

    class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Meeting
            fields = ['title', 'group']
    class PostOutSerializer(serializers.ModelSerializer):
        class Meta:
            model = Meeting
            fields = '__all__'

    def post(self, request: Request):

        # Get data from request
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not GroupMember.objects\
                .filter(group=serializer.validated_data['group'], user=request.user)\
                .exists():
            return Response(status=403)
        
        # Save meeting
        meeting = serializer.save()

        # Validate data
        out_serializer = self.PostOutSerializer(meeting)

        # Return meeting
        return Response(out_serializer.data)


class MeetingOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any meeting
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
                .exists():
            return Response(status=403)

        # Validate data
        serializer = MeetingPostSerializer(meeting)

        # Return meeting
        return Response(serializer.data)

    def patch(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = MeetingPostSerializer(meeting, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Validate data
        return Response(serializer.data)


class MeetingMemberAPIView(APIView):

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(serializers.ModelSerializer):
        class Meta:
            model = MeetingMember
            depth = 1
            fields = '__all__'

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting member
        meeting_members = MeetingMember.objects.filter(meeting=meeting)

        # Validate data
        out_serializer = self.GetOutSerializer(meeting_members, many=True)

        # Return meeting
        return Response(out_serializer.data)
    

class MeetingMessageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get meeting messages
        meeting_messages = MeetingMessage.objects.filter(meeting=meeting)

        # Validate data
        serializer = MeetingMessageSerializer(meeting_messages, many=True)

        # Return meeting
        return Response(serializer.data)

    def post(self, request: Request, meeting_id):
        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Get meeting member (GroupMemberを経由してユーザーを検索)
        group_member = get_object_or_404(
            GroupMember, 
            user=request.user, 
            group=meeting.group
            )

        # Get data from request
        serializer = MeetingMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=group_member, meeting=meeting)

        return Response(serializer.data)


class MeetingMessageOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, meeting_id, message_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
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
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
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
