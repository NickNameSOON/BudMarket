# models.py in 'order' app
from django.db import models
from django.contrib.auth.models import User
from market.models import Product

class Order(models.Model):
    PROCESSING = 'processing'
    PACKING = 'packing'
    DELIVERING = 'delivering'
    RECEIVED = 'received'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PROCESSING, 'Опрацювання'),
        (PACKING, 'Комплектація'),
        (DELIVERING, 'Доставляється'),
        (RECEIVED, 'Отримано покупцем'),
        (CANCELED, 'Відмінено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
