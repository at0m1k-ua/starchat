from django.contrib.auth.models import User
from django.db import models

from starchat.models.post import Post


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
