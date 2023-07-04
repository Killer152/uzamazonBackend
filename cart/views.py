from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from cart.serializers import CartAddProductSerializer, CartDetailSerializer, CartRemoveProductSerializer
from shop.models import ProductModel


class CartAddView(APIView):
    """Add product to user`s cart
    POST:
    {
        id: product`s id
        quantity: int
    }
    """
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        serializer = CartAddProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            product = get_object_or_404(ProductModel, id=data.get('id'))
            cart.add(product=product, quantity=data['quantity'])
            return Response({'message': 'Product was added successfully'})
        return Response(serializer.errors, status=status.HTTP_200_OK)


class CartRemoveView(APIView):
    """Removes product from cart
    POST:
    {
        id: product`s id
    }
    """
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        serializer = CartRemoveProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            product = get_object_or_404(ProductModel, id=data.get('id'))
            cart.remove(product)
            return Response({'message': 'Product was removed successfully'})
        return Response(serializer.errors, status=status.HTTP_200_OK)


class CartDetailView(APIView):
    """Detail info of cart"""
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        data = []
        for item in cart:
            i = CartDetailSerializer(item, context={'request': request})
            data.append(i.data)
        data = {
            'products': data,
            'sum': cart.get_total_price()
        }
        return Response(data=data)


class CartClearView(APIView):
    """Fully clear cart"""
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        return Response({'message': 'Cart was cleaned successfully'})


class CartLengthView(APIView):
    """Length of cart"""
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return Response({'cart_length': len(cart)})
