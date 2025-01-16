import typing

from django.contrib.auth.models import User


User = typing.NewType('User', User)
