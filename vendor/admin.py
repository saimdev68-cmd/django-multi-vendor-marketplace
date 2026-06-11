from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    list_display = (
        "store_name",
        "id",
        "owner",
        "status",
        "is_featured",
    )

    list_filter = (
        "status",
        "is_featured",
    )

    search_fields = (
        "store_name",
        "owner__email",
        "phone_number",
        "city",
        "country",
    )

    prepopulated_fields = {
        "slug": ("store_name",)
    }

    readonly_fields = (
        "created_at",
        "updated_at",
        "get_full_address",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "store_name", "slug", "description")
        }),
        ("Media", {
            "fields": ("logo", "banner")
        }),
        ("Contact Info", {
            "fields": ("phone_number", "country", "city", "address")
        }),
        ("Business Settings", {
            "fields": ("status", "is_featured", "commission_rate")
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at", "get_full_address")
        }),
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("owner")