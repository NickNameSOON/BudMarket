from django.db import models
from django.contrib.auth.models import User

class UserRegister(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=44)
    def __str__(self):
        return self.user.username



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images/profiles')
    contact = models.CharField(max_length=15, default=0 ,blank=True)

    def __str__(self):
        return self.user.username