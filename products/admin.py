from django.contrib import admin
from django.contrib import messages
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Core Taxonomy Details", {
            "fields": ("name", "slug", "icon"),
            "description": "Enter the primary category information and public-facing URL handles.",
        }),
        ("Status & Permissions", {
            "fields": ("is_active",),
            "classes": ("collapse",),
            "description": "Control the visibility of this category across Marketly stores.",
        }),
    )

    list_display = (
        "id",
        "name",
        "slug",
        "is_active",
        "created_at",
    )
    
    list_editable = ("is_active",)
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "slug", "=id")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)
    show_full_result_count = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_select_related = ["vendor", "category"]

    list_display = (
        "sku",
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
        "sku",
        "name",
        "vendor__store_name",  
        "category__name",
    )

    readonly_fields = (
        "slug",
        "sku",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Identification", {
            "fields": (
                "vendor",
                "category",
                "name",
                "slug",
                "description",
                "image",
            )
        }),
        ("Financial Inventory Matrix", {
            "fields": (
                "sku",
                "price",
                "discount_price",
                "stock"
            )
        }),
        ("Compliance & Visibility Control", {
            "fields": (
                "status",
                "is_featured",
            )
        }),
        ("System Meta Timestamps", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    actions = ["approve_products", "reject_products"]

    @admin.action(description="Approve selected listings and publish to marketplace")
    def approve_products(self, request, queryset):
        updated_count = queryset.update(status=Product.ProductStatus.ACTIVE)
        self.message_user(
            request, 
            f"Successfully updated status to Active for {updated_count} marketplace listings.",
            messages.SUCCESS
        )

    @admin.action(description="Reject selected listings and suspend from marketplace")
    def reject_products(self, request, queryset):
        updated_count = queryset.update(status=Product.ProductStatus.REJECTED)
        self.message_user(
            request, 
            f"Successfully updated status to Rejected for {updated_count} marketplace listings.",
            messages.WARNING
        )