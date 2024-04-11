from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'payment_method']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
