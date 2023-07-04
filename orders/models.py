from django.db import models

from account.models import UserModel
from shop.models import ProductModel


PAYMENT_TYPES = (
    (1, 'Наличные'),
    (2, 'Пластиковая карта'),
    (3, 'Click'),
    (4, 'Payme'),
)

PAYMENT_STATUS = (
    (1, 'В ожидании'),
    (2, 'Ошибка'),
    (3, 'Завершено'),
    (4, 'Отменен'),
    (5, 'Истёк'),
)

DELIVERY_STATUS = (
    (1, 'В ожидании'),
    (2, 'На доставке'),
    (3, 'Доставлен'),
)


class OrderModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='orders')
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10)
    apartment = models.CharField(max_length=10, null=True, blank=True)
    entrance = models.CharField(max_length=10, null=True, blank=True)
    floor = models.CharField(max_length=10, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    sum = models.IntegerField(default=0)

    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPES)
    payment_status = models.PositiveSmallIntegerField(choices=PAYMENT_STATUS, default=1)
    delivery_status = models.PositiveSmallIntegerField(choices=DELIVERY_STATUS, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order #{self.id}'

    @property
    def get_cart_total(self):
        return sum(item.get_cost() for item in self.order_items.all())

    @property
    def get_cart_items(self):
        return ', '.join([item.product.title for item in self.order_items.all()])

    class Meta:
        ordering = ('-created_at', )
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItemModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.PROTECT, related_name='order_items')
    product = models.ForeignKey(ProductModel, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.order.id) + ' | ' + str(self.product.title)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
