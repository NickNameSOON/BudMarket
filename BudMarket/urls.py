from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from market.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('market/', include("market.urls", namespace="market")),
    path('users/', include("users.urls", namespace="users")),
    path('cart/', include("cart.urls", namespace="cart")),
    path('order/', include("order.urls", namespace="order")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)