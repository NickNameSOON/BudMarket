from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Додайте будь-які інші поля користувача, які ви бажаєте зберегти
    # Наприклад:
    email = models.EmailField(max_length=254, unique=True)
    password1 = models.CharField(max_length=44)
    password2 = models.CharField(max_length=44)
    def __str__(self):
        return self.user.username
