from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    text = models.CharField(max_length=5000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
