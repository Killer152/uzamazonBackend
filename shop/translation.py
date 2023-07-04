from modeltranslation.translator import TranslationOptions, register
from .models import CategoryModel, SubCategoryModel, ProductTypeModel, ProductModel


@register(CategoryModel)
class CategoryOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('ru', )


@register(SubCategoryModel)
class SubCategoryOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('ru', )


@register(ProductTypeModel)
class ProductTypeOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('ru', )


@register(ProductModel)
class ProductOptions(TranslationOptions):
    fields = ('title', 'description', 'characteristics')
    required_languages = ('ru', )


