# apps/meeting/api_views.py
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
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, group_id: uuid.UUID):
        group = get_object_or_404(Group, id=group_id)
        
        if not GroupMember.objects.filter(
            group=group, 
            user=request.user
        ).exists():
            return Response(
                {"error": "You are not a member of this group"}, 
                status=403
            )

        meetings = Meeting.objects.filter(group=group)
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)

    def post(self, request: Request, group_id: uuid.UUID):
        group = get_object_or_404(Group, id=group_id)
        
        group_member = get_object_or_404(
            GroupMember, 
            group=group, 
            user=request.user
        )

        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save(group=group)
            
            # 作成者をミーティングメンバーとして追加
            MeetingMember.objects.create(
                meeting=meeting,
                member=request.user,
                nickname=group_member.nickname,
                is_admin=True
            )
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    




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
        # グループ取得
        group = get_object_or_404(Group, id=group_id)
        
        # 管理者権限チェック
        if not GroupMember.objects.filter(
            group=group, 
            user=request.user,
            is_admin=True  # 管理者権限が必要
        ).exists():
            return Response(
                {"error": "You need admin rights to add members"}, 
                status=403
            )

        # ミーティング取得
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)
        
        # メンバー追加処理
        serializer = MeetingMemberSerializer(data=request.data)
        if serializer.is_valid():
            # グループメンバーからニックネームを取得
            group_member = get_object_or_404(
                GroupMember,
                group=group,
                user=serializer.validated_data['member']
            )
            
            # ミーティングメンバーとして追加
            meeting_member = serializer.save(
                meeting=meeting,
                nickname=group_member.nickname
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
        # グループ取得
        group = get_object_or_404(Group, id=group_id)
        
        # グループメンバーチェック
        if not GroupMember.objects.filter(
            group=group, 
            user=request.user
        ).exists():
            return Response(
                {"error": "You are not a member of this group"}, 
                status=403
            )

        # ミーティング取得
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)
        
        # ミーティングメンバー取得
        meeting_member = get_object_or_404(
            MeetingMember, 
            meeting=meeting, 
            member=request.user
        )

        # シリアライザ処理
        serializer = MeetingMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(
                meeting=meeting,
                sender=meeting_member  # 送信者を設定
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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
