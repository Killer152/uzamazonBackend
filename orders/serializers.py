from rest_framework import serializers

from orders.models import OrderModel, OrderItemModel
from shop.serializers import ProductSerializer


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['city', 'district', 'street', 'house_number', 'apartment',
                  'entrance', 'floor', 'comment', 'payment_type']


class OrderInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['city', 'district', 'street', 'house_number', 'apartment', 'entrance', 'floor']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItemModel
        fields = ['product', 'quantity']


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['city', 'district', 'street', 'house_number', 'apartment',
                  'entrance', 'floor', 'comment', 'payment_type', 'sum',
                  'delivery_status', 'get_cart_items', 'created_at']


class OrderUpdateSerializer(serializers.ModelSerializer):
    payment_status = serializers.IntegerField(min_value=1, max_value=5, required=True)

    def update(self, instance, validated_data):

        return super(OrderUpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = OrderModel
        fields = ['payment_status', ]
