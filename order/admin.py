from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("buyer","status","payment_status","total_amount",)
    list_filter = ("status","payment_status",)
    search_fields = ("buyer__user__email",)
    readonly_fields = ("total_amount","created_at","updated_at")
    inlines = [OrderItemInline]

    fieldsets = (
        ("Order Info", {
            "fields": (
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
