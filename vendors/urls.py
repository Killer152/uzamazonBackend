from django.urls import path

from vendors.utils import ExampleExportView, EmployeeImportView
from vendors.views import VendorRegisterView, VendorAvatarView, VendorAllProductsView, VendorDetailView, \
    VendorStatisticsView, VendorProductAddView, VendorProductDeleteView, CategoryAndManufacturerListView, \
    VendorProductUpdateView, VendorProductStatisticView, VendorCabinetView, VendorBannerView

urlpatterns = [
    path('create', VendorRegisterView.as_view(), name='vendor-create'),
    path('avatar', VendorAvatarView.as_view(), name='vendor-avatar'),
    path('banner', VendorBannerView.as_view(), name='vendor-banner'),
    path('cabinet', VendorCabinetView.as_view(), name='vendor-cabinet'),
    path('detail/<int:id>', VendorDetailView.as_view(), name='vendor-detail'),
    path('statistics', VendorStatisticsView.as_view(), name='vendor-statistics'),
    path('products/list', VendorAllProductsView.as_view(), name='vendor-products-list'),
    path('products/add', VendorProductAddView.as_view(), name='vendor-product-add'),
    path('products/<slug:product>/delete', VendorProductDeleteView.as_view(), name='vendor-product-delete'),
    path('products/<slug:product>/update', VendorProductUpdateView.as_view(), name='vendor-product-update'),
    path('products/<slug:product>/statistic', VendorProductStatisticView.as_view(), name='vendor-product-statistic'),
    path('categories', CategoryAndManufacturerListView.as_view(), name='vendor-categories-and-manufacturers-list'),
    path('export', ExampleExportView.as_view(), name='vendor-product-example-export'),
    path('import', EmployeeImportView.as_view(), name='vendor-product-import'),
]
