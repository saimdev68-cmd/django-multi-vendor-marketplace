from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    # Speeds up processing and stops inline dropdown rendering N+1 queries
    readonly_fields = ("product", "quantity")
    can_delete = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # Eagerly loads relational graphs instantly
    list_select_related = ("buyer__user",)
    list_display = ("buyer", "created_at") 
    search_fields = ("buyer__user__email", "buyer__user__username")
    readonly_fields = ("created_at", "updated_at")
    inlines = [CartItemInline]

    fieldsets = (
        ("Buyer Info", {
            "fields": ("buyer",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )