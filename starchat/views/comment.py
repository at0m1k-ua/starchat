from rest_framework.permissions import IsAuthenticated

from starchat.models import Comment, Post
from starchat.requests import *
from starchat.services.auto_response import AutoResponseService
from starchat.services.censorship import CensorshipService
from starchat.views.base_crud import BaseCrudViewSet


class CommentViewSet(BaseCrudViewSet):
    queryset = Comment.objects.filter(is_banned=False)
    permission_classes = [IsAuthenticated]
    create_request_body = CreateCommentRequestBody
    update_request_url_params = UpdateCommentRequestUrlParams
    update_request_body = UpdateCommentRequestBody
    list_related_object_type = Post
    list_related_object_fk_name = 'post_id'
    list_request_params = ListCommentRequestParams

    def create_middleware(self, item):
        censor = CensorshipService()
        item.is_banned = censor.is_harmful(item.text)
        if not item.is_banned:
            AutoResponseService().register(item)

        return item
