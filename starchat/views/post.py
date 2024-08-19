from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from starchat.models import Post
from starchat.serializers import PostSerializer


class PostView(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def create(self, *args, **kwargs):
        data = self.request.data
        text = data['text']
        post = Post.objects.create(text=text, sender_id=self.request.user.id)
        post.save()
        serializer = PostSerializer(post)
        return Response(status=200, data=serializer.data)

    def list(self, *args, **kwargs):
        sender_id = self.request.GET.get('sender_id')
        sender = get_object_or_404(User, id=sender_id)
        posts = sender.post_set.all()
        serializer = PostSerializer(posts, many=True)
        return Response(status=200, data=serializer.data)

    def retrieve(self, *args, **kwargs):
        post_id = self.kwargs['id']
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(status=200, data=serializer.data)

    def update(self, *args, **kwargs):
        post_id = self.kwargs['id']
        post = get_object_or_404(Post, id=post_id)
        if post.sender_id != self.request.user.id:
            return Response(403)

        data = self.request.data
        post.text = data['text']
        post.save()
        serializer = PostSerializer(post)
        return Response(status=200, data=serializer.data)

    def destroy(self, *args, **kwargs):
        post_id = self.kwargs['id']
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return Response(200)
