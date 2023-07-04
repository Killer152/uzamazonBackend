from rest_framework import status
from rest_framework.generics import get_object_or_404, CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import ProductModel
from shop.serializers import ProductSerializer
from shop.utils import paginate
from vendors.models import VendorModel
from vendors.permissions import VendorPermission
from vendors.serializers import VendorRegistrationSerializer, VendorAvatarSerializer, VendorDetailSerializer, \
    VendorStatisticsSerializer, ProductCreateSerializer, CategoryAndManufacturerListSerializer, \
    VendorProductStatisticSerializer, VendorCabinetSerializer, VendorBannerSerializer


class VendorRegisterView(CreateAPIView):
    """Registration of a new vendor. He must have default user account
    POST:
    {
        title: str,
        phone: int,
        website: str,
        instagram: str,
        description: str,
        avatar: image
    }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VendorRegistrationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'user': self.request.user})
        return context


class VendorAvatarView(UpdateAPIView):
    """Updates vendor's avatar"""
    serializer_class = VendorAvatarSerializer
    permission_classes = [IsAuthenticated, VendorPermission]

    def get_object(self):
        return self.request.user.vendor


class VendorBannerView(UpdateAPIView):
    """Updates vendor's banner"""
    serializer_class = VendorBannerSerializer
    permission_classes = [IsAuthenticated, VendorPermission]

    def get_object(self):
        return self.request.user.vendor


class VendorCabinetView(RetrieveAPIView):
    """Detail info about vendor"""
    serializer_class = VendorCabinetSerializer
    permission_classes = [IsAuthenticated, VendorPermission]

    def get_object(self):
        return self.request.user.vendor


class VendorDetailView(RetrieveAPIView):
    """Detail info about vendor"""
    serializer_class = VendorDetailSerializer

    def get_object(self):
        return VendorModel.objects.get(id=self.kwargs['id'])


class VendorStatisticsView(RetrieveAPIView):
    """Statics about vendor`s products selling and loading
    Additional GET params:
        date_from: date,
        date_to: date
    """
    serializer_class = VendorStatisticsSerializer
    permission_classes = [IsAuthenticated, VendorPermission]

    def get_object(self):
        return self.request.user.vendor


class VendorProductStatisticView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, VendorPermission]
    serializer_class = VendorProductStatisticSerializer

    def get_object(self):
        return get_object_or_404(ProductModel, slug=self.kwargs['product'], vendor=self.request.user.vendor)


class VendorAllProductsView(ListAPIView):
    """All vendor`s products"""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, VendorPermission]

    def get_queryset(self):
        return ProductModel.objects.filter(vendor=self.request.user.vendor)

    def get(self, request, *args, **kwargs):
        return paginate(request, self.get_queryset(), self.get_serializer)


class VendorProductAddView(CreateAPIView):
    """Vendor adds new products"""
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated, VendorPermission]
    queryset = ProductModel.objects.all()


class VendorProductDeleteView(DestroyAPIView):
    """Vendor deletes product"""
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated, VendorPermission]
    queryset = ProductModel.objects.all()

    def get_object(self):
        return get_object_or_404(ProductModel, slug=self.kwargs['product'])

    def destroy(self, request, *args, **kwargs):
        if self.request.user.vendor == self.get_object().vendor:
            self.perform_destroy(self.get_object())
            return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You are not owner of this product", status=status.HTTP_403_FORBIDDEN)


class CategoryAndManufacturerListView(APIView):
    """List of all manufacturers, sub/categories and product types"""
    permission_classes = [IsAuthenticated, VendorPermission]

    def get(self, request):
        list = []
        return Response(CategoryAndManufacturerListSerializer(list, many=False).data)


class VendorProductUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, VendorPermission]
    serializer_class = ProductCreateSerializer
    queryset = ProductModel.objects.all()

    def get_object(self):
        return get_object_or_404(ProductModel, vendor=self.request.user.vendor, slug=self.kwargs['product'])
