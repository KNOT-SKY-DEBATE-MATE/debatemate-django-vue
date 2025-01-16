from rest_framework import serializers

from .models import (
    Group,
    GroupMember,
    GroupMessage
)


class GroupSerializer(serializers.ModelSerializer):

    """
    Serializer for Group model.
    """

    class Meta:

        # Model
        model = Group

        # Fields
        fields = [
            'id',
            'name',
            'description',
        ]

        # Extra kwargs
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'description': {'required': False},
        }


class GroupMemberSerializer(serializers.ModelSerializer):

    """
    Serializer for GroupMember model.
    """

    class Meta:

        # Model and fields
        model = GroupMember

        # Extract field depth
        depth = 1

        # Fields
        fields = [
            'id',
            'group',
            'user',
            'nickname',
            'is_banned',
            'is_admin',
        ]

        # Extra kwargs
        extra_kwargs = {
            'id': {'read_only': True},
            'group': {'read_only': True},
            'user': {'required': True},
        }


class GroupMessageSerializer(serializers.ModelSerializer):

    """
    Serializer for GroupMessage model.
    """

    class Meta:

        # Model and fields
        model = GroupMessage

        # Extract field depth
        depth = 1

        # Fields
        fields = [
            'id',
            'group',
            'sender',
            'content',
            'created_at',
            'updated_at',
        ]

        # Extra kwargs
        extra_kwargs = {
            'id': {'read_only': True},
            'group': {'required': True},
            'sender': {'required': True},
            'content': {'required': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
