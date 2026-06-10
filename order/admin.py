from django.contrib import admin
from .models import Order, OrderItem


# =========================
# ORDER ADMIN
# =========================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "buyer",
        "status",
        "payment_status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "buyer__user__username",
        "buyer__user__email",
    )

    readonly_fields = (
        "order_number",
        "total_amount",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Order Info", {
            "fields": (
                "order_number",
                "buyer",
                "shipping_address",
            )
        }),
        ("Status", {
            "fields": (
                "status",
                "payment_status",
                "total_amount",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


# =========================
# ORDER ITEM ADMIN
# =========================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "vendor",
        "price",
        "quantity",
    )

    list_filter = (
        "vendor",
    )

    search_fields = (
        "order__order_number",
        "product__name",
        "vendor__store_name",
    )

    readonly_fields = (
        "price",
    )