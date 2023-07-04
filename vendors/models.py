from django.db import models

from account.models import UserModel


class VendorModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.PROTECT, related_name='vendor')
    title = models.CharField(max_length=200)
    phone = models.CharField(max_length=13, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    avatar = models.ImageField(upload_to='vendor/profile/avatar/%Y/%m/%d', blank=True, null=True)
    banner = models.ImageField(upload_to='vendor/profile/banner/%Y/%m/%d', null=True, blank=True)
    sent_request = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + ' | ' + self.user.get_full_name()

    class Meta:
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'
