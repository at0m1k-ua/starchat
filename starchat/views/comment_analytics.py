from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from starchat.models import Comment
from starchat.requests.comment_analytics import CommentAnalyticsRequest


class CommentAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        param = CommentAnalyticsRequest(**request.GET.dict())
        comments_per_date = Comment.objects.filter(created_at__gte=param.date_from, created_at__lte=param.date_to)\
            .annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
        return Response(status=status.HTTP_200_OK, data=comments_per_date)
