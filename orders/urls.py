from django.urls import path

from orders.views import OrderCreateView, OrderInitView, CurrentOrderView, OrderHistoryView, OrderUpdateView

urlpatterns = [
    path('init', OrderInitView.as_view(), name='order-init'),
    path('create', OrderCreateView.as_view(), name='order-create'),
    path('detail', CurrentOrderView.as_view(), name='order-detail'),
    path('list', OrderHistoryView.as_view(), name='order-list'),
    path('update/<int:id>', OrderUpdateView.as_view(), name='order-update'),
]
