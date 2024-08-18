from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    text = models.CharField(max_length=5000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.CharField(max_length=5000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
