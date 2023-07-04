from django.db import models
from rest_framework.exceptions import ValidationError

from vendors.models import VendorModel


class LandingModel(models.Model):
    banner1 = models.ImageField(upload_to='landing/1', null=True, blank=True)
    banner2 = models.ImageField(upload_to='landing/2', null=True, blank=True)
    banner3 = models.ImageField(upload_to='landing/3', null=True, blank=True)

    def __str__(self):
        return 'landing ' + str(self.pk)

    class Meta:
        verbose_name = 'landing banner'
        verbose_name_plural = 'landing banners'


class CategoryModel(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, unique=True)
    preview = models.ImageField(upload_to='categories/previews', null=True, blank=True)
    banner1 = models.ImageField(upload_to='categories', null=True, blank=True)
    banner2 = models.ImageField(upload_to='categories', null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class SubCategoryModel(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name='subcategories')

    class Meta:
        verbose_name = 'sub-category'
        verbose_name_plural = 'sub-categories'
        unique_together = ('title', 'category')

    def __str__(self):
        return self.title + ' | ' + self.category.title


class ProductTypeModel(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    subcategory = models.ForeignKey(SubCategoryModel, on_delete=models.PROTECT, related_name='product_types')

    def __str__(self):
        return self.title + ' | ' + self.subcategory.title

    class Meta:
        verbose_name = 'product type'
        verbose_name_plural = 'product types'


class ManufacturerModel(models.Model):
    title = models.CharField(max_length=200)
    subcategory = models.ForeignKey(SubCategoryModel, on_delete=models.PROTECT, related_name='manufacturers')
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name='manufacturers')
    slug = models.CharField(max_length=200, unique=True)
    avatar = models.ImageField(upload_to='manufacturer/avatar/%Y/%m/%d', null=True, blank=True)
    banner1 = models.ImageField(upload_to='manufacturer/landing/avatar/%Y/%m/%d', null=True, blank=True)
    banner2 = models.ImageField(upload_to='manufacturer/landing/avatar/%Y/%m/%d', null=True, blank=True)

    class Meta:
        verbose_name = 'manufacturer'
        verbose_name_plural = 'manufacturers'
        unique_together = ('title', 'category')

    def __str__(self):
        return self.title


class ProductModel(models.Model):
    product_type = models.ForeignKey(ProductTypeModel, on_delete=models.PROTECT, related_name='products', null=True,
                                     blank=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategoryModel, on_delete=models.CASCADE, related_name='products')
    manufacturer = models.ForeignKey(ManufacturerModel, on_delete=models.PROTECT, related_name='products', null=True,
                                     blank=True)
    vendor = models.ForeignKey(VendorModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    description = models.TextField()
    characteristics = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    count = models.PositiveIntegerField()
    total_views = models.PositiveIntegerField(default=0)
    star_count = models.IntegerField(default=0)
    star_total = models.IntegerField(default=0)
    rate = models.FloatField(default=0)

    available = models.BooleanField(default=True)
    best = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super(ProductModel, self).__init__(*args, **kwargs)
        self.__original_count = self.count

    def save(self, *args, **kwargs):
        if self.count == 0:
            self.available = False
        elif self.count > 0:
            self.available = True
        else:
            raise ValidationError("Count can not be negative")
        try:
            self.rate = round(self.star_total / self.star_count, 2)
        except ZeroDivisionError:
            self.rate = 0
        super(ProductModel, self).save(*args, **kwargs)
        if self.count != self.__original_count:
            CountStatusModel.objects.create(product=self, count=self.count)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title + ' | ' + self.category.title


class CountStatusModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title + " | " + str(self.count)
