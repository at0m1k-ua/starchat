from rest_framework.permissions import IsAuthenticated

from starchat.models import Comment, Post
from starchat.requests import *
from starchat.serializers import CommentSerializer
from starchat.views.base_crud import BaseCrud


class CommentViewSet(BaseCrud):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    create_request_body = CreateCommentRequestBody
    update_request_url_params = UpdateCommentRequestUrlParams
    update_request_body = UpdateCommentRequestBody
    list_related_object_type = Post
    list_related_object_fk_name = 'post_id'
    list_request_params = ListCommentRequestParams
