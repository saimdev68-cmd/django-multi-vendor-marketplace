from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "buyer",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "buyer__user__username",
        "buyer__user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Buyer Info", {
            "fields": ("buyer",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart",
        "product",
        "quantity",
        "item_total",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "product__name",
        "cart__buyer__user__username",
    )

    readonly_fields = (
        "created_at",
        "item_total",
    )

    fieldsets = (
        ("Cart Info", {
            "fields": ("cart", "product", "quantity")
        }),
        ("Calculated Data", {
            "fields": ("item_total",)
        }),
        ("Timestamp", {
            "fields": ("created_at",)
        }),
    )

    def item_total(self, obj):
        return obj.total_price()

    item_total.short_description = "Total Price"