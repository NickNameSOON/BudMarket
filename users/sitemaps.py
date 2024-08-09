# users/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return User.objects.all()

    def location(self, item):
        return f'/users/{item.username}/'
