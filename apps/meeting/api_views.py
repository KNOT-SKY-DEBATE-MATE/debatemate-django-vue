# apps/meeting/api_views.py
import requests

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
    MeetingSerializer,
    MeetingMemberSerializer,
    MeetingMessageSerializer,
    MeetingMessageAnnotationSerializer
)



class MeetingAPIView(APIView):

    """
    List all meetings, or create a new meeting.    
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingSerializer):

        # Get group
        class Meta(MeetingSerializer.Meta):
            depth = 1

    def get(self, request: Request):

        # Get group
        meetings = Meeting.objects.filter(group__members__user=request.user)

        # Validate data
        out_serializer = self.GetOutSerializer(meetings, many=True)

        # Return group
        return Response(out_serializer.data)

    class PostSerializer(MeetingSerializer):

        # Fields to return
        class Meta(MeetingSerializer.Meta):
            fields = ['title', 'group', 'description']

    class PostOutSerializer(MeetingSerializer):

        # Inherit group serializer
        class Meta(MeetingSerializer.Meta):
            depth = 1

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

    """
    Retrieve, update or delete a meeting.    
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingSerializer):

        # Inherit group serializer
        class Meta(MeetingSerializer.Meta):
            depth = 1

    def get(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any meeting
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
                .exists():
            return Response(status=403)

        # Validate data
        out_serializer = self.GetOutSerializer(meeting)

        # Return meeting
        return Response(out_serializer.data)
    
    class PatchSerializer(MeetingSerializer):

        # Fields to return
        class Meta(MeetingSerializer.Meta):
            fields = ['title', 'description']

    class PatchOutSerializer(MeetingSerializer):

        # Inherit group serializer
        class Meta(MeetingSerializer.Meta):
            depth = 1

    def patch(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=meeting.group, user=request.user)\
                .exists():
            return Response(status=403)

        # Get data from request
        serializer = self.PatchSerializer(meeting, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save meeting
        meeting = serializer.save()

        # Validate data
        out_serializer = self.PatchOutSerializer(meeting)

        # Return meeting
        return Response(out_serializer.data)


class MeetingMemberAPIView(APIView):

    """
    List all meeting members, or create a new meeting member.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingMemberSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMemberSerializer.Meta):
            depth = 1

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

    """
    List all meeting messages, or create a new meeting message.
    """

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingMessageSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageSerializer.Meta):
            depth = 1

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
        out_serializer = self.GetOutSerializer(meeting_messages, many=True)

        # Return meeting
        return Response(out_serializer.data)
    
    class PostSerializer(MeetingMessageSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageSerializer.Meta):
            fields = ['content']

    class PostOutSerializer(MeetingMessageSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageSerializer.Meta):
            depth = 1

    def post(self, request: Request, meeting_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Get meeting member (GroupMemberを経由してユーザーを検索)
        group_member = get_object_or_404(GroupMember, user=request.user, group=meeting.group)

        # Get data from request
        serializer = self.PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save meeting
        meeting_message = serializer.save(sender=group_member, meeting=meeting)

        # Validate data
        out_serializer = self.PostOutSerializer(meeting_message)

        # Post event to websocket server
        try:
            response = requests.post(self.WEBSOCKET_URL + f'on/meeting/{meeting.id}/message/')
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            pass

        # Return meeting
        return Response(out_serializer.data)


class MeetingMessageOneAPIView(APIView):

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingMessageSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageSerializer.Meta):
            depth = 1

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
        out_serializer = MeetingMessageSerializer(meeting_message)

        # Return meeting
        return Response(out_serializer.data)
    
    class PatchSerializer(MeetingMessageSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageSerializer.Meta):
            fields = ['content']

    class PatchOutSerializer(MeetingMessageSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageSerializer.Meta):
            depth = 1

    def patch(self, request: Request, meeting_id, message_id):

        # Get meeting
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Get meeting message
        meeting_message = get_object_or_404(MeetingMessage, id=message_id, meeting=meeting)

        # Get data from request
        serializer = MeetingMessageSerializer(meeting_message, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Save meeting
        meeting_message = serializer.save()

        # Validate data
        out_serializer = MeetingMessageSerializer(meeting_message)

        # Return meeting
        return Response(out_serializer.data)


class MeetingMessageAnnotationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    class GetOutSerializer(MeetingMessageAnnotationSerializer):
        
        # Inherit group-member serializer and extract external fields
        class Meta(MeetingMessageAnnotationSerializer.Meta):
            depth = 1

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
            out_serializer = self.GetOutSerializer(meeting_message_annotation)
        
        except MeetingMessageAnnotation.DoesNotExist:

            # Get meeting
            out_serializer = MeetingMessageSerializer(meeting_message)

            try:
                # Get meeting-messages
                response = requests.post("...", json=out_serializer.data)
                response.raise_for_status()

            except requests.exceptions.HTTPError as err:

                # Return meeting
                return Response(status=err.response.status_code)
            
            # Validate data
            out_serializer = MeetingMessageAnnotationSerializer(data=response.json())
            out_serializer.is_valid(raise_exception=True)
            out_serializer.save(message=meeting_message, meeting=meeting)

        # Return meeting
        return Response(out_serializer.data)
