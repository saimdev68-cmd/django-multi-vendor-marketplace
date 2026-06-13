from django.contrib import admin, messages
from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
   
    list_display = (
        "vendor",
        "account_holder_name",
        "bank_name",
        "account_type",
        "is_verified",
        "created_at",
    )

    
    list_editable = ("is_verified",)

   
    list_filter = (
        "is_verified",
        "account_type",
        "bank_name",
        "created_at",
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
        ("Ownership Connection", {
            "fields": ("vendor",),
            "description": "The registered storefront owner linked to this settlement route."
        }),
        ("Financial Routing Details", {
            "fields": (
                "account_holder_name",
                "bank_name",
                "account_number",
                "iban_number",
                "account_type",
            )
        }),
        ("Compliance & Verification", {
            "fields": ("is_verified",),
            "classes": ("collapse",),  
        }),
        ("System Meta Logging", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    ordering = ("-created_at",)


    actions = ["bulk_verify_accounts", "bulk_unverify_accounts"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("vendor")

    
    @admin.action(description="Approve verification status for selected accounts")
    def bulk_verify_accounts(self, request, queryset):
        updated_count = queryset.update(is_verified=True)
        self.message_user(
            request,
            f"Successfully verified {updated_count} bank settlement route profiles.",
            messages.SUCCESS
        )

    @admin.action(description="Revoke verification status for selected accounts")
    def bulk_unverify_accounts(self, request, queryset):
        updated_count = queryset.update(is_verified=False)
        self.message_user(
            request,
            f"Successfully revoked verification for {updated_count} bank profiles.",
            messages.WARNING
        )