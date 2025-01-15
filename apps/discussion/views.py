import uuid

from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.http.request import HttpRequest

from apps.group.models import (
    Group,
    GroupMember,
)

from .models import (
    Discussion,
    DiscussionMember,
)


class DiscussionView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, group_id: uuid.UUID, discussion_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Check if user is a member of any group
        if not GroupMember.objects\
                .filter(group=group, user=request.user)\
                .exists():
            return HttpResponse(status=403)

        # Get discussion id
        discussion =\
            get_object_or_404(Discussion, id=discussion_id, group=group)

        # Check if user is a member of discussion
        if not DiscussionMember.objects\
                .filter(discussion=discussion, user=request.user)\
                .exists():
            return HttpResponse(status=403)

        # Render group
        return render(request, 'discussion.html', {
            'group': group,
            'user': request.user,
            'discussion': discussion,
        })
