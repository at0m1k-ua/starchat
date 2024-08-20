from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from starchat.models import Comment, Post
from starchat.requests import *
from starchat.serializers import CommentSerializer
from starchat.views.validated_mvs import ValidatedModelViewSet


class CommentViewSet(ValidatedModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def create(self, *args, **kwargs):
        body = self._pack_to_req_model(CreateCommentRequestBody, self.request.data)

        post = get_object_or_404(Post, id=body.post_id)
        comment_to_create = self.get_queryset().create(sender_id=self.request.user.id, post_id=post.id, text=body.text)
        comment_to_create.save()
        serializer = self.get_serializer(comment_to_create)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, *args, **kwargs):
        params = self._pack_to_req_model(ListCommentRequestParams, self.request.GET)

        post = get_object_or_404(Post, id=params.post_id)
        comments = post.comment_set.all()
        serializer = self.get_serializer(comments, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, *args, **kwargs):
        url_params = self._pack_to_req_model(RetrieveCommentUrlParams, self.kwargs)

        retrieved_comment = get_object_or_404(self.get_queryset(), id=url_params.id)
        serializer = self.get_serializer(retrieved_comment)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def update(self, *args, **kwargs):
        url_params = self._pack_to_req_model(UpdateCommentRequestUrlParams, self.kwargs)
        body = self._pack_to_req_model(UpdateCommentRequestBody, self.request.data)

        comment_to_uodate = get_object_or_404(self.get_queryset(), id=url_params.id)
        if comment_to_uodate.sender_id != self.request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment_to_uodate.text = body.text
        comment_to_uodate.save()
        serializer = self.get_serializer(comment_to_uodate)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def destroy(self, *args, **kwargs):
        url_params = self._pack_to_req_model(DestroyCommentRequestUrlParams, self.kwargs)

        comment_to_delete = get_object_or_404(self.get_queryset(), id=url_params.id)
        if comment_to_delete.sender_id != self.request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment_to_delete.delete()
        return Response(status.HTTP_200_OK)
