from django.contrib import admin
from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):

    list_display = (
        "vendor",
        "account_holder_name",
        "bank_name",
        "is_primary",
        "is_verified",
    )

    list_filter = (
        "account_type",
        "is_primary",
        "is_verified",
        "bank_name",
    )

    search_fields = (
        "vendor__store_name",
        "account_holder_name",
        "bank_name",
        "account_number",
        "iban_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Vendor Info", {
            "fields": ("vendor",)
        }),
        ("Bank Details", {
            "fields": (
                "account_holder_name",
                "bank_name",
                "account_number",
                "iban_number",
                "account_type",
            )
        }),
        ("Status", {
            "fields": (
                "is_verified",
                "is_primary",
            )
        }),
        ("System Info", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    ordering = ("-created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("vendor")