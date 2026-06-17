from django.contrib import admin
from .models import Wallet, Transaction  # Singular professional naming


class TransactionInline(admin.TabularInline):
    """
    Shows a clean list of a vendor's incoming and outgoing money 
    directly when viewing their wallet page.
    """
    model = Transaction
    extra = 0
    # Guard Rails: Financial ledger history should never be altered manually
    readonly_fields = ("transaction_type", "amount", "status", "reference_id", "description", "created_at")
    can_delete = False
    ordering = ("-created_at",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    Central control interface for managing and tracking vendor balances.
    """
    list_display = ("get_store_name", "available_balance", "pending_balance", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("vendor__store_name", "vendor__user__email")
    
    # Financial integrity: Force totals to be read-only to prevent unauthorized manual cash injections
    readonly_fields = ("vendor", "available_balance", "pending_balance", "created_at", "updated_at")
    
    inlines = [TransactionInline]

    @admin.display(description="Store Name", ordering="vendor__store_name")
    def get_store_name(self, obj):
        return obj.vendor.store_name


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    A comprehensive audit log that allows marketplace administrators 
    to easily inspect every transaction across the entire platform.
    """
    list_display = ("id", "get_store_name", "transaction_type", "amount", "status", "created_at")
    list_filter = ("transaction_type", "status", "created_at")
    search_fields = ("vendor__store_name", "reference_id", "description")
    
    # Lock down the entire model form to ensure audit records are completely immutable
    readonly_fields = ("wallet", "vendor", "amount", "transaction_type", "status", "reference_id", "description", "created_at")

    @admin.display(description="Store Name", ordering="vendor__store_name")
    def get_store_name(self, obj):
        return obj.vendor.store_name

    # Security: Prevent any administrative staff from manually creating or deleting transaction records
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False