from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

from .models import (
    Group,
    GroupMember,
    GroupMessage,
)

User = get_user_model()


class GroupMessageConsumer(AsyncWebsocketConsumer):

    """
    Activated on message to group
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user: User = None  # type: ignore
        self.group: Group = None  # type: ignore

    async def connect(self):

        # Get user
        user = self.scope['user']

        # Check if user is authenticated
        if not user.is_authenticated:

            # Close connection
            return await self.close()

        @database_sync_to_async
        def __get_group():
            return get_object_or_404(Group, id=self.scope['url_route']['kwargs']['group_id'])

        # Get group
        group = await __get_group()

        @database_sync_to_async
        def __get_check_groupmember():
            return GroupMember.objects\
                .filter(group=group, user=user)\
                .exists()

        # Check if user is a member of any group
        if not await __get_check_groupmember():

            # Close connection
            return await self.close()
        
        print("YasuiUnagi 4")
        
        # Set user and group
        self.user = user
        self.group = group

        # Accept
        return await self.accept()
    
    async def disconnect(self, close_code):

        # Get channel layer
        if self.user and self.group:
            
            # Get channel layer
            return await self.channel_layer.group_discard(str(self.group), str(self.user))

    async def on_message(self, event):

        # Get channel layer
        return await self.channel_layer.group_send(str(self.group), event)
