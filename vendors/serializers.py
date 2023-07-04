import datetime

from django.db import IntegrityError
from rest_framework import serializers, status

from orders.models import OrderItemModel
from shop.models import ProductModel, CategoryModel, ManufacturerModel, CountStatusModel
from shop.serializers import SubCategoryListSerializer, ManufacturerSerializer
from vendors.models import VendorModel
import unidecode
from unidecode import unidecode


class VendorRegistrationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        if VendorModel.objects.filter(user=user).exists():
            raise serializers.ValidationError({'message': 'Vendor by this user already registered',
                                               'status': status.HTTP_400_BAD_REQUEST})
        return VendorModel.objects.create(user=user, **validated_data, sent_request=True)

    class Meta:
        model = VendorModel
        fields = ['title', 'phone', 'website', 'instagram', 'description', 'avatar', 'banner']


class VendorAvatarSerializer(serializers.ModelSerializer):
    def save(self, *args, **kwargs):
        if self.instance.avatar:
            self.instance.avatar.delete()
        return super().save(**kwargs)

    class Meta:
        model = VendorModel
        fields = ['avatar']


class VendorBannerSerializer(serializers.ModelSerializer):
    def save(self, *args, **kwargs):
        if self.instance.banner:
            self.instance.banner.delete()
        return super().save(**kwargs)

    class Meta:
        model = VendorModel
        fields = ['banner']


class VendorCabinetSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['title', 'avatar', 'description', 'banner']


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['title', 'avatar', 'description', 'banner']


class VendorStatisticsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        date_from = self.context['request'].GET.get("date_from")
        date_to = self.context['request'].GET.get('date_to')
        qs = ProductModel.objects.filter(vendor=instance)
        count = 0
        all2 = 0
        dd = 0
        for a in qs:
            os = OrderItemModel.objects.filter(order__payment_status=3, product=a).distinct()
            om = CountStatusModel.objects.filter(product__vendor=instance, product=a).distinct()
            if date_from:
                d1 = datetime.datetime.strptime(date_from, "%Y-%m-%d").replace(hour=00, second=00)
                om = om.filter(created__gte=d1)
                os = os.filter(order__updated_at__gte=d1)
            if date_to:
                d2 = datetime.datetime.strptime(date_to, "%Y-%m-%d").replace(hour=23, second=59)
                om = om.filter(created__lte=d2)
                os = os.filter(order__updated_at__lte=d2)
            for b in os:
                count += b.quantity
            if om.exists():
                de = 0
                all2 += om.last().count
                for d in om:
                    if d.count > de:
                        dd += d.count - de
                    de = d.count
            else:
                all2 += 0
                dd = 0
        try:
            sold_percentage = round(count * 100 / dd, 2)
        except ZeroDivisionError:
            sold_percentage = 0
        data = {"all": all2,
                "load": dd,
                "sold": count,
                "sold_percentage": sold_percentage,
                "created": instance.created_at,
                "today": datetime.datetime.today()}
        return data

    class Meta:
        model = VendorModel
        fields = '__all__'


class VendorProductStatisticSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        date_from = self.context['request'].GET.get("date_from")
        date_to = self.context['request'].GET.get('date_to')
        om = CountStatusModel.objects.filter(product=instance)
        os = OrderItemModel.objects.filter(order__payment_status=3, product=instance).distinct()
        if date_from:
            d1 = datetime.datetime.strptime(date_from, "%Y-%m-%d").replace(hour=00, second=00)
            om = om.filter(created__gte=d1)
            os = os.filter(order__updated_at__gte=d1)
        if date_to:
            d2 = datetime.datetime.strptime(date_to, "%Y-%m-%d").replace(hour=23, second=59)
            om = om.filter(created__lte=d2)
            os = os.filter(order__updated_at__lte=d2)
        count = 0
        for a in os:
            count += a.quantity
        if om.exists():
            dd = 0
            de = 0
            all1 = om.last().count
            for d in om:
                if d.count > de:
                    dd += d.count - de
                de = d.count
        else:
            all1 = 0
            dd = 0
        try:
            sold_percentage = round(count * 100 / dd, 2)
        except ZeroDivisionError:
            sold_percentage = 0
        data = {"all": all1,
                "load": dd,
                "sold": count,
                "sold_percentage": sold_percentage,
                "created": instance.created,
                "today": datetime.datetime.today()}
        return data

    class Meta:
        model = ProductModel
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(min_value=0)

    def slug_product(self, validated_data):
        try:
            if validated_data['slug'] is not None:
                return ProductModel.objects.create(**validated_data)
        except KeyError:
            try:
                validated_data['slug'] = unidecode(validated_data['title'])
                return ProductModel.objects.create(**validated_data)
            except IntegrityError:
                slug = ProductModel.objects.get(slug=validated_data['slug']).slug
                validated_data['slug'] = slug + str(1)
                return self.slug_product(validated_data=validated_data)
        except IntegrityError:
            slug = list(ProductModel.objects.get(slug=validated_data['slug']).slug)
            slug[-1] = str(int(slug[-1]) + 1)
            validated_data['slug'] = "".join(slug)
            return self.slug_product(validated_data=validated_data)

    def create(self, validated_data):
        validated_data['vendor'] = self.context['request'].user.vendor
        pm = self.slug_product(validated_data=validated_data)
        CountStatusModel.objects.create(product=pm, count=validated_data['count'])
        return pm

    class Meta:
        model = ProductModel
        fields = ['title', 'product_type', 'category', 'subcategory', 'manufacturer', 'image', 'description',
                  'characteristics', 'price', 'count']


class CategoryListSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryModel
        fields = '__all__'


class CategoryAndManufacturerListSerializer(serializers.Serializer):
    manufacturers = serializers.SerializerMethodField('get_m')
    categories = serializers.SerializerMethodField('get_c')

    def get_m(self, obj):
        return ManufacturerSerializer(ManufacturerModel.objects.all(), many=True).data

    def get_c(self, obj):
        return CategoryListSerializer(CategoryModel.objects.all(), many=True).data
