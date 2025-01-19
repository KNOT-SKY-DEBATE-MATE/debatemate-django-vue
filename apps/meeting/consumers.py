# apps/meeting/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from .models import (
    Meeting,
    MeetingMember,
    MeetingMessage,
)

User = get_user_model()

class MeetingMessageConsumer(AsyncWebsocketConsumer):
    """
    Activated on message to meeting
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user: User = None  # type: ignore
        self.meeting: Meeting = None  # type: ignore

    async def connect(self):
        # Get user
        user = self.scope['user']

        # Check if user is authenticated
        if not user.is_authenticated:
            # Close connection
            return await self.close()

        @database_sync_to_async
        def __get_meeting():
            return get_object_or_404(Meeting, id=self.scope['url_route']['kwargs']['meeting_id'])

        # Get meeting
        meeting = await __get_meeting()

        @database_sync_to_async
        def __get_check_meetingmember():
            return MeetingMember.objects\
                .filter(meeting=meeting, member__user=user)\
                .exists()

        # Check if user is a member of the meeting
        if not await __get_check_meetingmember():
            # Close connection
            return await self.close()

        # Set user and meeting
        self.user = user
        self.meeting = meeting

        # Accept
        return await self.accept()

    async def disconnect(self, close_code):
        # Get channel layer
        if self.user and self.meeting:
            # Get channel layer
            return await self.channel_layer.group_discard(str(self.meeting), str(self.user))

    async def on_message(self, event):
        # Get channel layer
        return await self.channel_layer.group_send(str(self.meeting), event)