from django.contrib import admin
from .models import Order, VendorOrder, OrderItem


class OrderItemInline(admin.TabularInline):
    """Renders the historical immutable products inside a vendor bundle."""
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity", "get_subtotal")
    can_delete = False

    @admin.display(description="Subtotal")
    def get_subtotal(self, obj: OrderItem) -> str:
        return f"${obj.total_price}"


@admin.register(VendorOrder)
class VendorOrderAdmin(admin.ModelAdmin):
    """Enables clear operational views for isolated fulfillment tracking packages."""
    list_select_related = ("order__buyer__user", "vendor")
    list_display = ("id", "get_order_id", "vendor", "status", "vendor_subtotal")
    list_filter = ("status", "updated_at")
    search_fields = ("id", "order__id", "vendor__name", "tracking_number")
    inlines = [OrderItemInline]
    
    readonly_fields = ("order", "vendor", "vendor_subtotal", "updated_at")

    @admin.display(ordering="order__id", description="Global Order ID")
    def get_order_id(self, obj: VendorOrder) -> str:
        return f"#{obj.order.id}"


class VendorOrderInline(admin.StackedInline):
    """Nests the isolated fulfillment packages cleanly within the global financial order."""
    model = VendorOrder
    extra = 0
    show_change_link = True  # Allows admins to jump straight into individual lines for full product listings
    readonly_fields = ("vendor", "vendor_subtotal", "status")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # --- Performance Optimization ---
    # Stops the N+1 database trap by grouping related user models in 1 JOIN
    list_select_related = ("buyer__user", "country", "city")

    list_display = ("id", "get_buyer_email", "payment_status", "total_amount", "created_at")
    list_filter = ("payment_status", "created_at")
    search_fields = ("id", "buyer__user__email", "name", "stripe_payment_intent_id")
    
    readonly_fields = ("total_amount", "stripe_payment_intent_id", "created_at", "updated_at")
    inlines = [VendorOrderInline]

    fieldsets = (
        ("Customer Identity", {
            "fields": ("buyer", "name", "phone_number")
        }),
        ("Fulfillment Destination", {
            "fields": ("country", "city", "shipping_address")
        }),
        ("Financial Transaction Ledger", {
            "fields": ("payment_status", "total_amount", "stripe_payment_intent_id")
        }),
        ("System Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    @admin.display(ordering="buyer__user__email", description="Buyer Email")
    def get_buyer_email(self, obj: Order) -> str:
        return obj.buyer.user.email