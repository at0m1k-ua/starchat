from rest_framework.serializers import ModelSerializer

from starchat.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
