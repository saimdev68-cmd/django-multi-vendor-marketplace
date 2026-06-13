from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ("buyer","created_at")
    search_fields = ("buyer__user__email",)
    readonly_fields = ("created_at","updated_at")
    inlines = [CartItemInline]

    fieldsets = (
        ("Buyer Info", {
            "fields": ("buyer",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )