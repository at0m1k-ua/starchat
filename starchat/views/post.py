from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from starchat.models import Post
from starchat.requests import *
from starchat.serializers import PostSerializer
from starchat.views.validated_mvs import ValidatedModelViewSet


class PostViewSet(ValidatedModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def create(self, *args, **kwargs):
        body = self._pack_to_req_model(CreatePostRequestBody, self.request.data)

        post_to_create = self.get_queryset().create(text=body.text, sender_id=self.request.user.id)
        post_to_create.save()
        serializer = self.get_serializer(post_to_create)
        return Response(status=200, data=serializer.data)

    def list(self, *args, **kwargs):
        params = self._pack_to_req_model(ListPostRequestParams, self.request.GET)

        sender = get_object_or_404(User, id=params.sender_id)
        posts = sender.post_set.all()
        serializer = self.get_serializer(posts, many=True)
        return Response(status=200, data=serializer.data)

    def retrieve(self, *args, **kwargs):
        url_params = self._pack_to_req_model(RetrievePostUrlParams, self.kwargs)

        retrieved_post = get_object_or_404(self.get_queryset(), id=url_params.id)
        serializer = self.get_serializer(retrieved_post)
        return Response(status=200, data=serializer.data)

    def update(self, *args, **kwargs):
        url_params = self._pack_to_req_model(UpdatePostRequestUrlParams, self.kwargs)
        body = self._pack_to_req_model(UpdatePostRequestBody, self.request.data)

        post_to_update = get_object_or_404(self.get_queryset(), id=url_params.id)
        if post_to_update.sender_id != self.request.user.id:
            return Response(403)

        post_to_update.text = body.text
        post_to_update.save()
        serializer = self.get_serializer(post_to_update)
        return Response(status=200, data=serializer.data)

    def destroy(self, *args, **kwargs):
        url_params = self._pack_to_req_model(DestroyPostRequestUrlParams, self.kwargs)

        post_to_delete = get_object_or_404(self.get_queryset(), id=url_params.id)
        post_to_delete.delete()
        return Response(200)
