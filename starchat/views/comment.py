from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from starchat.models import Comment
from starchat.serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def create(self, *args, **kwargs):
        pass

    def list(self, *args, **kwargs):
        pass

    def retrieve(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def destroy(self, *args, **kwargs):
        pass

