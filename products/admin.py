from django.contrib import admin
from .models import Category , Product
 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 1. Structured Layout Panels (Fieldsets)
    fieldsets = (
        ("Core Taxonomy Details", {
            "fields": ("name", "slug", "icon"),
            "description": "Enter the primary category information and public-facing URL handles.",
        }),
        ("Status & Permissions", {
            "fields": ("is_active",),
            "classes": ("collapse",),  # Can be expanded or collapsed by the admin
            "description": "Control the visibility of this category across Marketly stores.",
        }),
    )

    # 2. Layout Columns for List Dashboard
    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
    )
    
    # 3. Quick Global Quality-of-Life Toggles
    list_editable = ("is_active",)
    
    # 4. Optimized Filter & Search Components
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "slug", "=id")
    
    # 5. Real-Time UI Mirroring Configuration
    prepopulated_fields = {"slug": ("name",)}
    
    # 6. Performance & Scale Optimizations
    ordering = ("-created_at",)
    show_full_result_count = False

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