# apps/meeting/views.py
import uuid

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import render, get_object_or_404
from django.views import View
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
from .serializers import (
    MeetingSerializer,
    MeetingMemberSerializer,
)


class MeetingView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, group_id: uuid.UUID, meeting_id: uuid.UUID):
        # グループを取得
        group = get_object_or_404(Group, id=group_id)

        # ミーティングIDを取得
        meeting = get_object_or_404(Meeting, id=meeting_id, group=group)

        # ユーザーがミーティングのメンバーかどうかを確認
        if not MeetingMember.objects\
                .filter(meeting=meeting, member=request.user)\
                .exists():
            return HttpResponse(status=403)

        # グループをレンダリング
        return render(request, 'meeting.html', {
            'group': group,
            'user': request.user,
            'meeting': meeting,
        })


class MeetingListView(generics.ListCreateAPIView):
    """
    グループのミーティングリストの取得と作成
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        """
        指定されたグループのミーティングリストを取得
        """
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return Meeting.objects.filter(group=group)

    def create(self, request, *args, **kwargs):
        """
        ミーティング作成時のエラーデバッグと詳細なバリデーション
        """
        # リクエストデータのログ出力
        print("Received Meeting Create Data:", request.data)

        # グループIDの取得
        group_id = self.kwargs.get('group_id')
        
        # リクエストデータにグループIDを追加
        request.data['group'] = str(group_id)

        # シリアライザの作成と検証
        serializer = self.get_serializer(data=request.data)
        
        try:
            # バリデーション
            serializer.is_valid(raise_exception=True)
            
            # ミーティング作成
            self.perform_create(serializer)
            
            # レスポンス
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        except Exception as e:
            # エラーの詳細ログ出力
            print("Meeting Create Error:", str(e))
            print("Validation Errors:", serializer.errors)
            return Response(
                {"error": str(e), "details": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        """
        ミーティングを作成
        """
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        
        # グループのメンバーであることを確認
        group_member = get_object_or_404(GroupMember, group=group, member=self.request.user)
        
        # ミーティングを作成
        meeting = serializer.save(group=group)
        
        # 作成者をミーティングメンバーに追加
        MeetingMember.objects.create(meeting=meeting, member=self.request.user)


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    特定のミーティングの詳細、更新、削除
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingSerializer

    def get_queryset(self):
        """
        指定されたグループとミーティングのクエリセットを取得
        """
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return Meeting.objects.filter(group=group)

    def get_object(self):
        """
        特定のミーティングを取得
        """
        queryset = self.get_queryset()
        meeting_id = self.kwargs.get('meeting_id')
        obj = get_object_or_404(queryset, id=meeting_id)
        return obj

    def check_object_permissions(self, request, obj):
        """
        オブジェクトに対する権限を確認
        """
        # ミーティングメンバーであることを確認
        if not MeetingMember.objects.filter(meeting=obj, member=request.user).exists():
            self.permission_denied(
                request,
                message='このミーティングにアクセスする権限がありません。',
                code='not_meeting_member'
            )
        return super().check_object_permissions(request, obj)