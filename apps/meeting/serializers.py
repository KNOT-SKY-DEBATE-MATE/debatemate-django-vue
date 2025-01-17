# apps/meeting/serializers.py

from rest_framework import serializers

from .models import (
    Meeting,
    MeetingMember,
    MeetingMessage,
    MeetingMessageAnnotation
)


class MeetingSerializer(serializers.ModelSerializer):
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
            'group': {'read_only': True},
            'title': {'required': True},
        }


class MeetingMemberSerializer(serializers.ModelSerializer):
    """
    MeetingMember モデル用のシリアライザ
    """

    class Meta:
        # シリアライザに関連するモデル
        model = MeetingMember

        # シリアライズするフィールド
        fields = [
            'id',
            'meeting',
            'member',
        ]

        # フィールド固有のオプション
        extra_kwargs = {
            'id': {'read_only': True},
            'meeting': {'read_only': True},
            'member': {'required': True},
        }


class MeetingMessageSerializer(serializers.ModelSerializer):
    """
    MeetingMessage モデル用のシリアライザ
    """

    class Meta:
        # シリアライザに関連するモデル
        model = MeetingMessage

        # シリアライズするフィールド
        fields = [
            'id',
            'meeting',
            'sender',
            'content',
            'created_at',
            'updated_at',
        ]

        # フィールド固有のオプション
        extra_kwargs = {
            'id': {'read_only': True},
            'meeting': {'required': True},
            'sender': {'required': True},
            'content': {'required': True},
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