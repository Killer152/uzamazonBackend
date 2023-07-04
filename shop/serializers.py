from rest_framework import serializers

from shop.models import CategoryModel, SubCategoryModel, ManufacturerModel, ProductModel, ProductTypeModel, LandingModel


class LandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingModel
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerModel
        exclude = ['category']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeModel
        exclude = ['subcategory']


class SubCategoryListSerializer(serializers.ModelSerializer):
    product_types = ProductTypeSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategoryModel
        fields = '__all__'


class Test(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryModel
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.products.count()

    class Meta:
        model = CategoryModel
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'title', 'slug', 'image', 'price', 'rate', 'count']


class ProductDetailSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    def get_rate(self, obj):
        try:
            return obj.star_total / obj.star_count
        except ZeroDivisionError:
            return 0

    class Meta:
        model = ProductModel
        exclude = ['created', 'updated', 'star_count', 'star_total']
        depth = 1
