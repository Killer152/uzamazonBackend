from django.contrib import admin

from shop.models import CategoryModel, ProductModel, SubCategoryModel, ManufacturerModel, ProductTypeModel, \
    LandingModel, CountStatusModel


@admin.register(LandingModel)
class LandingAdmin(admin.ModelAdmin):
    list_display = ['id', 'banner1', 'banner2', 'banner3']


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SubCategoryModel)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ManufacturerModel)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'count', 'available', 'best', 'category', 'manufacturer', 'rate']
    list_filter = ['available', 'created', 'updated', ]
    list_editable = ['price', 'available', 'best', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ProductTypeModel)
class ProductTypeModel(admin.ModelAdmin):
    list_display = ['title', 'subcategory', ]
    list_filter = ['subcategory', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(CountStatusModel)
class ProductTypeModel(admin.ModelAdmin):
    list_display = ['product', 'count']
