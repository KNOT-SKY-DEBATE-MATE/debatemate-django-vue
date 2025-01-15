import bleach
import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    PermissionsMixin
)


class User(AbstractUser, PermissionsMixin):

    """
    A user group in the system.
    """

    # User ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def save(self, *args, **kwargs):
        """
        Sanitize username and email
        """

        # Sanitize username
        self.username = bleach.clean(self.username)

        # Sanitize email
        self.email = bleach.clean(self.email)

        # Sanitize first name
        self.first_name = bleach.clean(self.first_name)

        # Sanitize last name
        self.last_name = bleach.clean(self.last_name)

        # Save
        super(User, self).save(*args, **kwargs)
