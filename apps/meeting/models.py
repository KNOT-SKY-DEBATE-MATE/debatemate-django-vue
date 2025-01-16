import bleach
import uuid

from django.db import models


class Meeting(models.Model):

    """
    Discussion Model
    """

    # Unique ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # Fields
    group = models.ForeignKey('group.Group', on_delete=models.CASCADE)

    # Fields
    title = models.CharField(max_length=255)

    # Fields
    description = models.TextField(max_length=1024, blank=True)

    # Fields
    is_archived = models.BooleanField(default=False)

    class Meta:

        # Model options
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'

        # Constraints
        constraints = [
            # Unique constraint for group and title
            models.UniqueConstraint(
                fields=['group', 'title'], name='unique_group_title'),
        ]

    def save(self, *args, **kwargs):

        # Sanitize title
        self.title = bleach.clean(self.title)

        # Sanitize description
        self.description = bleach.clean(self.description)

        # Save
        super(Meeting, self).save(*args, **kwargs)


class MeetingMember(models.Model):

    """
    Discussion Member Model
    """

    # Fields
    meeting = models.ForeignKey(
        to=Meeting,
        on_delete=models.CASCADE, related_name='meetingmember')

    # Fields
    member = models.ForeignKey(
        to='auth.User',
        on_delete=models.CASCADE, related_name='meetingmember')

    # Fields
    is_kicked = models.BooleanField(default=False)

    class Meta:

        # Model options
        verbose_name = 'Meeting Member'
        verbose_name_plural = 'Meeting Members'

        # Constraints
        constraints = [
            # Unique constraint for meeting and user
            models.UniqueConstraint(
                fields=['meeting', 'user'], name='unique_meeting_user'),
            # Unique constraint for meeting and nickname
            models.UniqueConstraint(
                fields=['meeting', 'nickname'], name='unique_meeting_member_nickname')
        ]

    def save(self, *args, **kwargs):

        # Sanitize nickname
        self.nickname = bleach.clean(self.nickname)

        # Save
        super(MeetingMember, self).save(*args, **kwargs)


class MeetingMessage(models.Model):

    """
    Discussion Message Model
    """

    # Fields
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    # Fields
    sender = models.ForeignKey(MeetingMember, on_delete=models.CASCADE)

    # Fields
    content = models.TextField(max_length=1024, blank=True)

    # Fields
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        # Model options
        verbose_name = 'Meeting Message'
        verbose_name_plural = 'Meeting Messages'

        # Ordering
        ordering = ['-created_at']

    def save(self, *args, **kwargs):

        # Sanitize content
        self.content = bleach.clean(self.content)

        # Save
        super(MeetingMessage, self).save(*args, **kwargs)


class MeetingMessageAnnotation(models.Model):

    """
    Discussion Message Summary Model
    """

    # Fields
    message = models.ForeignKey(MeetingMessage, on_delete=models.CASCADE)

    # Fields
    summary = models.TextField(max_length=255, blank=True)

    # Fields
    suggestions = models.TextField(max_length=255, blank=True)

    # Fields
    criticism = models.TextField(max_length=255, blank=True)

    # Fields
    warning = models.TextField(max_length=255, blank=True)

    class Meta:

        # Model options
        verbose_name = 'Meeting Message Annotation'
        verbose_name_plural = 'Meeting Message Annotations'

    def save(self, *args, **kwargs):

        # Sanitize summary
        self.summary = bleach.clean(self.summary)

        # Sanitize suggestions
        self.suggestions = bleach.clean(self.suggestions)

        # Sanitize criticism
        self.criticism = bleach.clean(self.criticism)

        # Sanitize warning
        self.warning = bleach.clean(self.warning)

        # Save
        super(MeetingMessageAnnotation, self).save(*args, **kwargs)
