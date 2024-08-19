from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from starchat.models import Comment, Post
from starchat.requests import CreateCommentRequestBody
from starchat.serializers import CommentSerializer
from starchat.views.validated_mvs import ValidatedModelViewSet


class CommentViewSet(ValidatedModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def create(self, *args, **kwargs):
        body = self._pack_to_req_model(CreateCommentRequestBody, self.request.data)

        post = get_object_or_404(Post, id=body.post_id)
        comment_to_create = self.get_queryset().create(sender_id=self.request.user.id, post_id=post.id, text=post.text)
        comment_to_create.save()
        serializer = self.get_serializer(comment_to_create)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, *args, **kwargs):
        pass

    def retrieve(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def destroy(self, *args, **kwargs):
        pass

