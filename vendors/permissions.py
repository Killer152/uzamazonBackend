from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from account.models import UserModel


class VendorPermission(BasePermission):
    def has_permission(self, request, view):
        if get_object_or_404(UserModel, id=request.user.id, vendor__isnull=False):
            return True
        else:
            return False
