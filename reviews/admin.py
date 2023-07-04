from django.contrib import admin

from reviews.models import ReviewModel


@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'stars']
