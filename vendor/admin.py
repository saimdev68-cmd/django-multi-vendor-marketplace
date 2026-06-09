from django.contrib import admin
from .models import Vendor, BankAccount

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):

    list_display = (
        "store_name",
        "owner__email",
        "phone_number",
        "status",
        "is_verified",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "status",
        "is_verified",
        "is_featured",
    )

    search_fields = (
        "store_name",
        "phone_number",
        "owner__email",
    )

    prepopulated_fields = {"slug": ("store_name",)}

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "owner",
                "store_name",
                "slug",
                "description",
                "logo",
                "banner",
            )
        }),
        ("Contact Info", {
            "fields": (
                "phone_number",
                "city",
                "address",
            )
        }),
        ("Status & Control", {
            "fields": (
                "status",
                "is_verified",
                "is_featured",
                "commission_rate",
            )
        }),
        ("Stats", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):

    list_display = (
        "vendor",
        "account_holder_name",
        "bank_name",
        "account_type",
        "is_primary",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "bank_name",
        "account_type",
        "is_primary",
        "is_verified",
    )

    search_fields = (
        "vendor__store_name",
        "account_holder_name",
        "account_number",
        "iban_number",
        "swift_code",
    )

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Vendor", {
            "fields": ("vendor",)
        }),
        ("Bank Details", {
            "fields": (
                "account_holder_name",
                "bank_name",
                "account_number",
                "iban_number",
                "swift_code",
                "account_type",
            )
        }),
        ("Status", {
            "fields": (
                "is_primary",
                "is_verified",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )