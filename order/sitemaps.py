# order/sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Order  # Import your model

class OrderSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Order.objects.all()

    def location(self, item):
        return f'/order/{item.id}/'
