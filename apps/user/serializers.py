from rest_framework import serializers
from django.contrib.auth.models import User 



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

        # Extra kwargs
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'password': {'write_only': True},
        }
