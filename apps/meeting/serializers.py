from rest_framework import serializers

from .models import (
    Meeting,
    MeetingMember,
    MeetingMessage,
    MeetingMessageAnnotation
)


class MeetingSerializer(serializers.ModelSerializer):

    """
    Serializer for the Discussion model.
    """

    class Meta:

        # The model associated with the serializer
        model = Meeting

        # The fields to be serialized
        fields = [
            'id',
            'group',
            'title',
            'description',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'group': {'read_only': True},
            'title': {'required': True},
        }


class MeetingMemberSerializer(serializers.ModelSerializer):

    """
    Serializer for the DiscussionMember model.
    """

    class Meta:

        # The model associated with the serializer
        model = MeetingMember

        # The fields to be serialized
        fields = [
            'id',
            'meeting',
            'user',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'meeting': {'read_only': True},
            'user': {'required': True},
        }


class MeetingMessageSerializer(serializers.ModelSerializer):

    """
    Serializer for the DiscussionMessage model.
    """

    class Meta:

        # The model associated with the serializer
        model = MeetingMessage

        # The fields to be serialized
        fields = [
            'id',
            'meeting',
            'sender',
            'content',
            'created_at',
            'updated_at',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'meeting': {'required': True},
            'sender': {'required': True},
            'content': {'required': True},
        }


class MeetingMessageAnnotationSerializer(serializers.ModelSerializer):

    """
    Serializer for the DiscussionMessageAnnotation model.
    """

    class Meta:

        # The model associated with the serializer
        model = MeetingMessageAnnotation

        # The fields to be serialized
        fields = [
            'id',
            'message',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'message': {'required': True},
        }
