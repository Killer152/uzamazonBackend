from django.urls import path

from cart.views import CartAddView, CartDetailView, CartRemoveView, CartClearView, CartLengthView

urlpatterns = [
    path('add/', CartAddView.as_view(), name='cart-add'),
    path('remove/', CartRemoveView.as_view(), name='cart-remove'),
    path('detail/', CartDetailView.as_view(), name='cart-detail'),
    path('clean/', CartClearView.as_view(), name='cart-clean'),
    path('length/', CartLengthView.as_view(), name='cart-length'),
]
