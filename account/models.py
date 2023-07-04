from django.contrib.auth import get_user_model
from django.db import models

from django.utils.translation import ugettext_lazy as _


GENDERS = (
    ('woman', _('Woman')),
    ('man', _('Man')),
)


UserModel = get_user_model()


class TokenModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='tokens')
    code = models.CharField(max_length=5)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' | ' + self.code

    class Meta:
        verbose_name = 'token'
        verbose_name_plural = 'tokens'


class ProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDERS)
    avatar = models.ImageField(upload_to='profiles', blank=True, null=True)

    def __str__(self):
        return self.user.username + ' | ' + self.user.get_full_name()

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

