from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.cart import Cart
from orders.models import OrderModel, OrderItemModel
from orders.serializers import OrderCreateSerializer, OrderInitSerializer, OrderDetailSerializer, OrderItemSerializer, \
    OrderUpdateSerializer
from shop.models import ProductModel
from shop.utils import paginate
from rest_framework.exceptions import NotAcceptable


class OrderInitView(GenericAPIView):
    """Initiate user`s order"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderInitSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        orders = OrderModel.objects.filter(user=user)
        address = ''
        if orders:
            address = orders.first()
            address = self.get_serializer(address).data
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'address': address
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OrderCreateView(CreateAPIView):
    """Creates user`s order
    POST:
    {
        city: str,
        district: str,
        street: str,
        house_number: str,
        apartment: str,
        entrance: str,
        floor: str,
        comment: str,
        payment_type: int
    }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart(self.request)
        if len(cart) == 0:
            raise ValidationError({'message': 'Empty cart', 'status': False})
        for item in cart:
            if item['product'].count < item['quantity']:
                raise NotAcceptable("There are no such quantities for these products")
        order = OrderModel.objects.create(user=user, sum=cart.get_total_price(), **serializer.validated_data)

        for item in cart:
            OrderItemModel.objects.create(order=order, product=item['product'], quantity=item['quantity'])
            item['product'].count = item['product'].count - item['quantity']
            item['product'].save()
        cart.clear()


class CurrentOrderView(GenericAPIView):
    """Displays current order"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order = OrderModel.objects.filter(user=self.request.user).first()
        products = OrderItemModel.objects.filter(order=order)
        order = OrderDetailSerializer(order)
        products = OrderItemSerializer(products, many=True, context={'request': request})
        data = {
            'order': order.data,
            'order_items': products.data
        }
        return Response(data=data, status=status.HTTP_200_OK)


class OrderHistoryView(ListAPIView):
    """User`s all orders"""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItemModel.objects.filter(order__user=self.request.user).order_by('order')

    def get(self, request, *args, **kwargs):
        return paginate(request, self.get_queryset(), self.get_serializer)


class OrderUpdateView(UpdateAPIView):
    serializer_class = OrderUpdateSerializer
    queryset = OrderModel.objects.all()
    lookup_url_kwarg = 'id'
