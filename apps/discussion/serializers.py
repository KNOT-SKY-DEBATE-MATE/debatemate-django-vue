from rest_framework import serializers

from .models import (
    Discussion,
    DiscussionMember,
    DiscussionMessage,
    DiscussionMessageAnnotation
)


class DiscussionSerializer(serializers.ModelSerializer):

    class Meta:

        # The model associated with the serializer
        model = Discussion

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


class DiscussionMemberSerializer(serializers.ModelSerializer):

    class Meta:

        # The model associated with the serializer
        model = DiscussionMember

        # The fields to be serialized
        fields = [
            'id',
            'discussion',
            'user',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'discussion': {'read_only': True},
            'user': {'required': True},
        }


class DiscussionMessageSerializer(serializers.ModelSerializer):

    class Meta:

        # The model associated with the serializer
        model = DiscussionMessage

        # The fields to be serialized
        fields = [
            'id',
            'discussion',
            'sender',
            'content',
            'created_at',
            'updated_at',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'discussion': {'required': True},
            'sender': {'required': True},
            'content': {'required': True},
        }


class DiscussionMessageAnnotationSerializer(serializers.ModelSerializer):

    class Meta:

        # The model associated with the serializer
        model = DiscussionMessageAnnotation

        # The fields to be serialized
        fields = [
            'id',
            'message',
            'sender',
            'content',
        ]

        # Field-specific options
        extra_kwargs = {
            'id': {'read_only': True},
            'message': {'required': True},
            'sender': {'required': True},
            'content': {'required': True},
        }
