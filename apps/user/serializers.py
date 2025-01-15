from rest_framework import serializers

from .models import (
    User
)


class UserSerializer(serializers.ModelSerializer):

    """
    Serializer for user.
    """

    class Meta:

        # Get model and fields
        model = User

        # Fields
        fields = [
            'id',
            'username',
            'password',
        ]

        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'password': {'required': True, 'write_only': True},
        }
