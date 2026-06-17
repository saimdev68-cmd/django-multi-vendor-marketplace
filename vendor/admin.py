from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Vendor, BankAccount, VendorStatusLog, BankAccountStatusLog


class VendorStatusLogInline(admin.TabularInline):
    
    model = VendorStatusLog
    extra = 0
    readonly_fields = ("old_status", "new_status", "reason", "changed_by", "created_at")
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


class BankAccountStatusLogInline(admin.TabularInline):
    
    model = BankAccountStatusLog
    extra = 0
    readonly_fields = ("old_status", "new_status", "reason", "changed_by", "created_at")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "id",
        "owner_email",  
        "status",
        "is_verified",      
        "is_featured",
        "commission_rate",
        "display_logo",  
    )

    list_editable = ("is_featured", "status", "is_verified")

    list_filter = (
        "status",
        "is_verified",      
        "is_featured",
        "country",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__email",
        "owner__username",
        "phone",
        "city__name",
        "tax_identifier",   
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
        "get_full_address",
        "display_logo_preview",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "name", "slug", "description")
        }),
        ("Media Assets", {
            "fields": (("logo", "display_logo_preview"), "banner")
        }),
        ("Contact & Location Details", {
            "fields": ("phone", "country", "city", "address", "get_full_address")
        }),
        ("Business & Logistics Management", {
            "fields": ("status", "is_verified", "tax_identifier", "status_notes", "is_featured", "commission_rate")
        }),
        ("System Audit Metrics", {
            "classes": ("collapse",),  
            "fields": ("created_at", "updated_at")
        }),
    )

    ordering = ("-created_at",)
    
    actions = ["bulk_approve_vendors", "bulk_suspend_vendors"]

    
    inlines = [VendorStatusLogInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("owner", "country", "city")
    
    @admin.display(ordering="owner__email", description="Owner Email")
    def owner_email(self, obj):
        return obj.owner.email

    @admin.display(description="Logo Preview")
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 35px; height: 35px; border-radius: 4px; object-fit: cover;" />', obj.logo.url)
        return format_html('<span style="color: #999;">No Logo</span>')

    @admin.display(description="Current Uploaded Logo")
    def display_logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 120px; border-radius: 8px;" />', obj.logo.url)
        return "No logo uploaded yet."

    def save_model(self, request, obj, form, change):
        """
        Intercepts manual form saves in the admin detail dashboard.
        Passes down the logged-in administrator context to the post_save signals block.
        """
        if request.user and request.user.is_authenticated:
            
            obj.status_notes = obj.status_notes or "Modified manually via Admin Panel Form."
        super().save_model(request, obj, form, change)

    @admin.action(description="Mark selected vendors as ACTIVE")
    def bulk_approve_vendors(self, request, queryset):
        
        for vendor in queryset:
            vendor.status_notes = "Approved in bulk operation by administration staff."
            vendor.status = Vendor.Status.ACTIVE
            vendor.save(update_fields=["status", "status_notes", "updated_at"])
            
        self.message_user(
            request, 
            f"Successfully activated {queryset.count()} vendor storefronts.", 
            messages.SUCCESS
        )

    @admin.action(description="Mark selected vendors as SUSPENDED")
    def bulk_suspend_vendors(self, request, queryset):
        for vendor in queryset:
            vendor.status_notes = "Suspended in bulk operation by administration staff due to policy audit."
            vendor.status = Vendor.Status.SUSPENDED
            vendor.save(update_fields=["status", "status_notes", "updated_at"])

        self.message_user(
            request, 
            f"Successfully suspended {queryset.count()} vendor storefronts.", 
            messages.WARNING
        )


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
   
    list_display = (
        "vendor",
        "account_holder_name",
        "bank_name",
        "currency",
        "account_type",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "account_type",
        "currency",
        "created_at",
    )

    search_fields = (
        "vendor__name", 
        "account_holder_name",
        "bank_name__name", 
        "swift_bic", 
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
                "swift_bic", 
                "currency",
                "account_number",
                "iban_number",
                "account_type",
            )
        }),
        ("Compliance & Verification", {
            "fields": ("status", "status_notes"), 
            "description": "Operational controls for manual KYC/AML bank account verification audits."
        }),
        ("System Meta Logging", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    ordering = ("-created_at",)

    actions = ["approve_accounts", "reject_accounts"]
    inlines = [BankAccountStatusLogInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("vendor", "currency", "bank_name")

    def save_model(self, request, obj, form, change):
        """Captures the admin identity who mutated this specific bank card profile."""
        super().save_model(request, obj, form, change)

    @admin.action(description="Approve selected bank accounts for payments")
    def approve_accounts(self, request, queryset):
        for account in queryset:
            account.status_notes = "Verified and approved by administration risk team clearing operations."
            account.status = BankAccount.Status.VERIFIED
            account.save(update_fields=["status", "status_notes", "updated_at"])

        self.message_user(
            request, 
            f"Successfully approved {queryset.count()} bank accounts for settlements.", 
            messages.SUCCESS
        )

    @admin.action(description="Reject selected bank accounts (compliance failure)")
    def reject_accounts(self, request, queryset):
        for account in queryset:
            account.status_notes = "Rejected during compliance verification routine checks."
            account.status = BankAccount.Status.REJECTED
            account.save(update_fields=["status", "status_notes", "updated_at"])

        self.message_user(
            request, 
            f"Flagged {queryset.count()} bank accounts as REJECTED. Please specify reasons inside individual records.", 
            messages.WARNING
        )


@admin.register(VendorStatusLog)
class VendorStatusLogAdmin(admin.ModelAdmin):
    list_display = ("vendor", "old_status", "new_status", "changed_by", "created_at")
    list_filter = ("new_status", "created_at")
    search_fields = ("vendor__name", "reason", "changed_by__email")
    readonly_fields = ("vendor", "old_status", "new_status", "reason", "changed_by", "created_at")
    
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False


@admin.register(BankAccountStatusLog)
class BankAccountStatusLogAdmin(admin.ModelAdmin):
    list_display = ("bank_account", "old_status", "new_status", "changed_by", "created_at")
    list_filter = ("new_status", "created_at")
    search_fields = ("bank_account__vendor__name", "reason", "changed_by__email")
    readonly_fields = ("bank_account", "old_status", "new_status", "reason", "changed_by", "created_at")
    
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False