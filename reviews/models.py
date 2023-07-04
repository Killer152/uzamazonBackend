from django.db import models

from account.models import UserModel
from shop.models import ProductModel


class ReviewModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='reviews')
    stars = models.SmallIntegerField()
    image_1 = models.ImageField(null=True, blank=True)
    image_2 = models.ImageField(null=True, blank=True)
    image_3 = models.ImageField(null=True, blank=True)
    image_4 = models.ImageField(null=True, blank=True)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title + ' | ' + self.user.get_full_name()

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
