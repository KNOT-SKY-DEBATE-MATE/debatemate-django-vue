# apps/meeting/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Meeting,
    MeetingMessage,
    MeetingMessageAnnotation
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MeetingGetSerializer(serializers.ModelSerializer):
    class Meta:
        # シリアライザに関連するモデル
        model = Meeting

        # シリアライズする深さ
        depth = 1

        # シリアライズするフィールド
        fields = [
            'id',
            'group',
            'title',
            'description',
        ]

class MeetingPostSerializer(serializers.ModelSerializer):
    """
    Meeting モデル用のシリアライザ
    """

    class Meta:
        # シリアライザに関連するモデル
        model = Meeting

        # シリアライズするフィールド
        fields = [
            'id',
            'group',
            'title',
            'description',
        ]

        # フィールド固有のオプション
        extra_kwargs = {
            'id': {'read_only': True},
            'group': {'required': True},
            'title': {'required': True},
        }


class MeetingMessageSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = MeetingMessage
        depth = 1
        fields = [
            'id',
            'meeting',
            'sender',
            'content',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'meeting': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

class MeetingMessageAnnotationSerializer(serializers.ModelSerializer):
    """
    MeetingMessageAnnotation モデル用のシリアライザ
    """

    class Meta:
        # シリアライザに関連するモデル
        model = MeetingMessageAnnotation

        # シリアライズするフィールド
        fields = [
            'id',
            'message',
        ]

        # フィールド固有のオプション
        extra_kwargs = {
            'id': {'read_only': True},
            'message': {'required': True},
        }