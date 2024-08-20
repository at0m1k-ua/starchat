from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from starchat.models import Post
from starchat.requests import *
from starchat.serializers import PostSerializer
from starchat.services.censorship import CensorshipService
from starchat.views.base_crud import BaseCrud


class PostViewSet(BaseCrud):
    queryset = Post.objects.filter(is_banned=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    create_request_body = CreatePostRequestBody
    update_request_url_params = UpdatePostRequestUrlParams
    update_request_body = UpdatePostRequestBody
    list_related_object_type = User
    list_related_object_fk_name = 'sender_id'
    list_request_params = ListPostRequestParams

    def create_middleware(self, item):
        censor = CensorshipService()
        item.is_banned = censor.is_harmful(item.text)
        return item
