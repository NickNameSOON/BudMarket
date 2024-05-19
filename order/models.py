from django.db import models
from django.contrib.auth.models import User
from market.models import Product


class Order(models.Model):
    PROCESSING = 'Опрацювання'
    PACKING = 'Комплектація'
    DELIVERING = 'Доставляється'
    RECEIVED = 'Отримано покупцем'
    CANCELED = 'Відмінено'

    STATUS_CHOICES = [
        (PROCESSING, 'Опрацювання'),
        (PACKING, 'Комплектація'),
        (DELIVERING, 'Доставляється'),
        (RECEIVED, 'Отримано покупцем'),
        (CANCELED, 'Відмінено'),
    ]

    PICKUP = 'Самовиніс'
    DELIVERY = 'Доставка'

    DELIVERY_CHOICES = [
        (PICKUP, 'Самовивіз з магазину'),
        (DELIVERY, 'Доставка'),
    ]

    CASH = 'Готівка'
    CARD = 'Карта'

    PAYMENT_CHOICES = [
        (CASH, 'Готівка'),
        (CARD, 'Карткою'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)
    delivery_method = models.CharField(max_length=10, choices=[('delivery', 'Доставка'), ('pickup', 'Самовивіз')])
    payment_method = models.CharField(max_length=10, choices=[('card', 'Кредитна карта'), ('cash', 'Готівка')])
    delivery_address = models.CharField(max_length=100, null=True, blank=True)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)

    def calculate_total_price(self):
        total_price = sum(item.price * item.quantity for item in self.orderitem_set.all())
        self.total_price = total_price
        self.save()


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255)

    def __str__(self):
        return f"Payment {'success' if self.success else 'failure'} on {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

