import bleach
import uuid

from django.db import models


class Discussion(models.Model):

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
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'

        # Indexes
        indexes = [
            models.Index(fields=['group', 'title']),
        ]

    def save(self, *args, **kwargs):

        # Sanitize title
        self.title = bleach.clean(self.title)

        # Sanitize description
        self.description = bleach.clean(self.description)

        # Save
        super(Discussion, self).save(*args, **kwargs)


class DiscussionMember(models.Model):

    """
    Discussion Member Model
    """

    # Fields
    discussion = models.ForeignKey(
        to=Discussion,
        on_delete=models.CASCADE, related_name='discussionmember')

    # Fields
    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE, related_name='discussionmember')

    # Fields
    nickname = models.CharField(max_length=255)

    # Fields
    is_kicked = models.BooleanField(default=False)

    class Meta:

        # Model options
        verbose_name = 'Discussion Member'
        verbose_name_plural = 'Discussion Members'

        # Constraints
        constraints = [
            # Unique constraint for discussion and user
            models.UniqueConstraint(
                fields=['discussion', 'user'], name='unique_discussion_user'),
            # Unique constraint for discussion and nickname
            models.UniqueConstraint(
                fields=['discussion', 'nickname'], name='unique_discussion_member_nickname')
        ]

    def save(self, *args, **kwargs):

        # Save
        super(DiscussionMember, self).save(*args, **kwargs)


class DiscussionMessage(models.Model):

    """
    Discussion Message Model
    """

    # Fields
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    # Fields
    sender = models.ForeignKey(DiscussionMember, on_delete=models.CASCADE)

    # Fields
    content = models.TextField(max_length=1024, blank=True)

    # Fields
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        # Model options
        verbose_name = 'Discussion Message'
        verbose_name_plural = 'Discussion Messages'

    def save(self, *args, **kwargs):

        # Sanitize content
        self.content = bleach.clean(self.content)

        # Save
        super(DiscussionMessage, self).save(*args, **kwargs)


class DiscussionMessageAnnotation(models.Model):

    """
    Discussion Message Summary Model
    """

    # Fields
    message = models.ForeignKey(DiscussionMessage, on_delete=models.CASCADE)

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
        verbose_name = 'Discussion Message Summary'
        verbose_name_plural = 'Discussion Message Summaries'

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
        super(DiscussionMessageAnnotation, self).save(*args, **kwargs)
