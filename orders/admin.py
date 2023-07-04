from django.contrib import admin

from orders.models import OrderModel, OrderItemModel


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_cart_items', 'sum', 'city', 'street', 'payment_type', 'payment_status', 'delivery_status']
    list_filter = ['user', 'city', 'payment_type', 'payment_status', 'delivery_status']
    search_fields = ['user', 'get_cart_items', 'street']
    list_editable = ['delivery_status', 'payment_status']


@admin.register(OrderItemModel)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity']
    list_filter = ['order', 'product']
    ordering = ['order']
