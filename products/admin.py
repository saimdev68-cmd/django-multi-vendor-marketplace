from django.contrib import admin
from .models import Category , Product
 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "id",
        'slug',
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("id",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "vendor",
        "category",
        "price",
        "stock",
        "status",
        "is_featured",
        "created_at",
    )

    list_filter = (
        "status",
        "is_featured",
        "category",
        "vendor",
        "created_at",
    )

    search_fields = (
        "name",
        "vendor__store_name",
        "category__name",
    )

    prepopulated_fields = {"slug": ("name",)}

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": (
                "vendor",
                "category",
                "name",
                "slug",
                "description",
                "image",
            )
        }),
        ("Pricing & Stock", {
            "fields": (
                "price",
                "discount_price",
                "stock"
            )
        }),
        ("Control", {
            "fields": (
                "status",
                "is_featured",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )