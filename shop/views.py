from PIL import Image
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, RetrieveAPIView, GenericAPIView, UpdateAPIView, \
    DestroyAPIView
from rest_framework.response import Response

from shop.models import CategoryModel, ManufacturerModel, SubCategoryModel, ProductModel, LandingModel
from shop.search_product import search_product
from shop.serializers import CategoryListSerializer, ManufacturerSerializer, SubCategoryListSerializer, \
    ProductSerializer, ProductDetailSerializer, LandingSerializer
from shop.utils import paginate, filter_products
from vendors.permissions import VendorPermission


class LandingView(ListAPIView):
    """Here you can handle banners for the main page"""
    serializer_class = LandingSerializer
    queryset = LandingModel.objects.all()

    def get_object(self):
        return LandingModel.objects.order_by('-pk').first()


class LandingUpdateDeleteView(DestroyAPIView, UpdateAPIView):
    """Update or delete one of the banners
    PUT:
    {
        banner: number of banner(1-3),
        image: new image
    }
    DELETE:
    {
        banner: number of banner(1-3)
    }

    """
    permission_classes = [VendorPermission]
    lookup_url_kwarg = 'id'
    serializer_class = LandingSerializer

    def put(self, request, *args, **kwargs):
        landing = get_object_or_404(LandingModel, id=self.kwargs['id'])
        if self.request.data.get('banner') and self.request.FILES.get('image'):
            image = self.request.FILES.get('image')
            try:
                trial_image = Image.open(image)
                trial_image.load()
                if hasattr(image, 'reset'):
                    image.reset()
                trial_image = Image.open(image)
                trial_image.verify()
            except:
                return Response("Invalid image", status=status.HTTP_400_BAD_REQUEST)
            banner = int(self.request.data.get('banner'))
            if banner == 1:
                landing.banner1 = image
            elif banner == 2:
                landing.banner2 = image
            elif banner == 3:
                landing.banner3 = image
            else:
                return Response("Wrong banner number", status=status.HTTP_400_BAD_REQUEST)
            landing.save()
            return Response("Updated", status=status.HTTP_200_OK)
        return Response("No params", status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        landing = get_object_or_404(LandingModel, id=self.kwargs['id'])
        if self.request.data.get('banner'):
            banner = int(self.request.data.get('banner'))
            if banner == 1:
                landing.banner1 = None
            elif banner == 2:
                landing.banner2 = None
            elif banner == 3:
                landing.banner3 = None
            else:
                return Response("Wrong banner number", status=status.HTTP_400_BAD_REQUEST)
            landing.save()
            return Response("Deleted", status=status.HTTP_200_OK)
        return Response("No params", status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(ListAPIView):
    """Displays the list of categories and its subcategories"""
    queryset = CategoryModel.objects.order_by('id')
    serializer_class = CategoryListSerializer


class ManufacturerListView(ListAPIView):
    """Displays a list of manufacturers"""
    queryset = ManufacturerModel.objects.order_by('id')
    serializer_class = ManufacturerSerializer


class ManufacturerDetailView(GenericAPIView):
    """Displays all information needed for manufacturer view (manufacturer itself, subcategories in which this
    manufacturer in, and products of this manufacturer"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = ProductModel.objects.filter(manufacturer__slug=self.kwargs['manufacturer'])
        return filter_products(self.request, products)

    def get(self, request, *args, **kwargs):
        slug = kwargs['manufacturer']
        manufacturer = ManufacturerModel.objects.filter(slug=slug)
        if not manufacturer.exists():
            return HttpResponseNotFound()
        manufacturer = ManufacturerSerializer(manufacturer.get(), context={"request": request})
        subcategories = SubCategoryModel.objects.filter(manufacturers__slug=slug)
        subcategories = SubCategoryListSerializer(subcategories, many=True, context={"request": request})
        return paginate(request, self.get_queryset(), self.get_serializer, info=manufacturer,
                        subcategories=subcategories)


class CategoryDetailView(GenericAPIView):
    """Displays a list of products for a particular category.
    Also enables sorting and ordering (?sort_by=expensive/cheap, ?manufacturer={manufacturer id),
    ?product_type={product_type id), ?max_price={int}, min_price={int}"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = ProductModel.objects.filter(category__slug=self.kwargs['category'])
        return filter_products(self.request, products)

    def get(self, request, *args, **kwargs):
        subcategories = SubCategoryModel.objects.filter(category__slug=self.kwargs['category'])
        subcategories = SubCategoryListSerializer(subcategories, many=True, context={"request": request})
        manufacturers = ManufacturerModel.objects.filter(category__slug=self.kwargs['category'])
        manufacturers = ManufacturerSerializer(manufacturers, many=True, context={"request": request})
        category = CategoryModel.objects.filter(slug=self.kwargs['category']).get()
        category = CategoryListSerializer(category, context={"request": request})
        return paginate(request, self.get_queryset(), self.get_serializer, subcategories=subcategories,
                        manufacturers=manufacturers, info=category)


class ProductDetailView(RetrieveAPIView):
    """Product page endpoint"""
    serializer_class = ProductDetailSerializer

    def get_object(self):
        pm = get_object_or_404(ProductModel, slug=self.kwargs['product'])
        pm.total_views += 1
        pm.save()
        return pm


class ProductBestView(ListAPIView):
    """List of all best products"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = ProductModel.objects.filter(best=True)
        return filter_products(self.request, products)

    def get(self, request, *args, **kwargs):
        manufacturers = ManufacturerModel.objects.filter(products__in=self.get_queryset()).distinct()
        manufacturers = ManufacturerSerializer(manufacturers, many=True, context={"request": request})
        categories = CategoryModel.objects.filter(products__in=self.get_queryset()).distinct()
        categories = CategoryListSerializer(categories, many=True, context={"request": request})
        subcategories = SubCategoryModel.objects.filter(products__in=self.get_queryset()).distinct()
        subcategories = SubCategoryListSerializer(subcategories, many=True, context={"request": request})
        return paginate(request, self.get_queryset(), self.get_serializer, manufacturers=manufacturers,
                        categories=categories, subcategories=subcategories)


# class ProductDeleteView(DestroyAPIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = ProductSerializer
#     lookup_url_kwarg = 'product'
#
#     def get_object(self):
#         return get_object_or_404(ProductModel, slug=self.kwargs['product'])
#
#     def perform_destroy(self, instance):
#         if self.request.user == instance.user:
#             return super().perform_destroy(instance)


class SearchView(GenericAPIView):
    """Main search
    GET params:
        search: name of product and/or manufacturer

    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = ProductModel.objects.select_related('manufacturer').all()
        if self.request.GET.get('search'):
            products = search_product(self.request.GET.get('search').lower(), products)
        return filter_products(self.request, products)

    def get(self, request, *args, **kwargs):
        pm = search_product(self.request.GET.get('search').lower(),
                            ProductModel.objects.select_related('manufacturer').all())
        manufacturers = ManufacturerModel.objects.filter(
            products__in=pm).distinct()
        manufacturers = ManufacturerSerializer(manufacturers, many=True, context={"request": request})
        categories = CategoryModel.objects.filter(products__in=pm).distinct()
        categories = CategoryListSerializer(categories, many=True, context={"request": request})
        subcategories = SubCategoryModel.objects.filter(products__in=pm).distinct()
        subcategories = SubCategoryListSerializer(subcategories, many=True, context={"request": request})
        return paginate(request, self.get_queryset(), self.get_serializer, manufacturers=manufacturers,
                        categories=categories, subcategories=subcategories)
