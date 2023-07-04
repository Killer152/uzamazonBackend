from django.contrib import admin

from vendors.models import VendorModel


@admin.register(VendorModel)
class VendorAdmin(admin.ModelAdmin):
    def vendor_owner(self, obj):
        return obj.user.get_full_name()

    list_display = ['title', 'vendor_owner', 'phone', 'sent_request', 'verified', 'vendor_owner']
    list_filter = ['created_at']
    list_editable = ['verified']
    search_fields = ['title']
