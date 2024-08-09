# bot/models.py
from django.db import models
from django.contrib.auth.models import User

class BotUserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}..."
