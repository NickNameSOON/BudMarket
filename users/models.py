from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    contactNumber = models.CharField(max_length=15, default='', blank=True)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    DeliveryAddress = models.CharField(max_length=100, blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    instance.user.save()
