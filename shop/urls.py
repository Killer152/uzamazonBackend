from django.urls import path

from shop.views import CategoryListView, ManufacturerDetailView, ProductDetailView, \
    CategoryDetailView, LandingView, ProductBestView, SearchView, LandingUpdateDeleteView, ManufacturerListView

urlpatterns = [
    path('landing', LandingView.as_view(), name='landing'),
    path('landing/<int:id>', LandingUpdateDeleteView.as_view(), name='landing-delete-update'),
    path('best', ProductBestView.as_view(), name='best'),
    path('category/list', CategoryListView.as_view(), name='category-list'),
    path('category/<slug:category>', CategoryDetailView.as_view(), name='category-detail'),

    path('manufacturer/<slug:manufacturer>', ManufacturerDetailView.as_view(), name='manufacturer-detail'),
    path('manufacturer/list', ManufacturerListView.as_view(), name='manufacturer-list'),

    path('product/search', SearchView.as_view(), name='product-search'),
    path('product/<slug:product>', ProductDetailView.as_view(), name='product-detail'),
    # path('product/<slug:product>/delete', ProductDeleteView.as_view(), name='product-delete'),
]
