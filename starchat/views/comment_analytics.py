from django.db.models import Count, Case, When, IntegerField
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
        comments_per_date = Comment.objects.annotate(
            date=TruncDate('created_at')
        ).filter(
            date__gte=param.date_from,
            date__lte=param.date_to
        ).values('date').annotate(
            banned_count=Count(Case(When(is_banned=True, then=1), output_field=IntegerField())),
            not_banned_count=Count(Case(When(is_banned=False, then=1), output_field=IntegerField())),
        ).order_by('date')
        return Response(status=status.HTTP_200_OK, data=comments_per_date)
