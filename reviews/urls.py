from django.urls import path

from reviews.views import ReviewCreateView, ReviewListView, ReviewDetailView

urlpatterns = [
    path('<slug:product>/create', ReviewCreateView.as_view(), name='review-create'),
    path('<slug:product>/list', ReviewListView.as_view(), name='review-list'),
    path('<slug:product>/detail', ReviewDetailView.as_view(), name='review-review'),
]
