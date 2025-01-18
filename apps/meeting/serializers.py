# apps/meeting/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    Meeting,
    MeetingMember,
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


class MeetingMemberSerializer(serializers.ModelSerializer):
    """
    MeetingMember モデル用のシリアライザ
    """
    user = UserSerializer(source='member', read_only=True)
    class Meta:
        # シリアライザに関連するモデル
        model = MeetingMember

        # シリアライズするフィールド
        fields = [
            'id',
            'meeting',
            'member',
            'nickname',
            'is_admin',
            'is_kicked',
            'user',
        ]

        # フィールド固有のオプション
        extra_kwargs = {
            'id': {'read_only': True},
            'meeting': {'read_only': True},
            'member': {'required': True},
            'is_admin': {'read_only': True},
        }


class MeetingMessageSerializer(serializers.ModelSerializer):
    sender = MeetingMemberSerializer(read_only=True)

    class Meta:
        model = MeetingMessage
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
            'meeting': {'read_only': True},  # required=Trueを削除
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