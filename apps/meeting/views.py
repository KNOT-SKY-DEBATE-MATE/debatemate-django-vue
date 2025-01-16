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
    Meeting,
    MeetingMember,
)


class MeetingView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest, group_id: uuid.UUID, meeting_id: uuid.UUID):

        # Get group
        group = get_object_or_404(Group, id=group_id)

        # Get meeting id
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # Check if user is a member of meeting
        if not MeetingMember.objects\
                .filter(meeting=meeting, user=request.user)\
                .exists():
            return HttpResponse(status=403)

        # Render group
        return render(request, 'meeting.html', {
            'group': group,
            'user': request.user,
            'meeting': meeting,
        })
