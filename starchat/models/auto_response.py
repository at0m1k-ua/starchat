from django.contrib.auth.models import User
from django.db import models


class AutoResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timeout = models.IntegerField(default=0)
