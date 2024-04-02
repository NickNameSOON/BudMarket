from django.db import models
from django.contrib.auth.models import User
from market.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def get_total_price(self):
        total_price = 0
        for item in self.cartitem_set.all():
            total_price += item.product.get_price() * item.quantity
        return total_price


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
