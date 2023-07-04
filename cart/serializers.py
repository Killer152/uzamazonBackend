from rest_framework import serializers

from shop.serializers import ProductSerializer


class CartAddProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    quantity = serializers.IntegerField()


class CartRemoveProductSerializer(serializers.Serializer):
    id = serializers.CharField()


class CartDetailSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    price = serializers.CharField()
    product = ProductSerializer()
    total_price = serializers.CharField()
