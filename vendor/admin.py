from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Vendor , Country , City


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "id",
        "owner_email",  
        "status",
        "is_verified",      
        "is_featured",
        "commission_rate",
        "display_logo",  
    )

    list_editable = ("is_featured", "status", "is_verified")

    list_filter = (
        "status",
        "is_verified",      
        "is_featured",
        "country",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__email",
        "owner__username",
        "phone",
        "city__name",
        "tax_identifier",   
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
        "get_full_address",
        "display_logo_preview",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "name", "slug", "description")
        }),
        ("Media Assets", {
            "fields": (("logo", "display_logo_preview"), "banner")
        }),
        ("Contact & Location Details", {
            "fields": ("phone", "country", "city", "address", "get_full_address")
        }),
        ("Business & Logistics Management", {
            "fields": ("status", "is_verified", "tax_identifier", "status_notes", "is_featured", "commission_rate")
        }),
        ("System Audit Metrics", {
            "classes": ("collapse",),  
            "fields": ("created_at", "updated_at")
        }),
    )

    ordering = ("-created_at",)
    
    actions = ["bulk_approve_vendors", "bulk_suspend_vendors"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("owner", "country", "city")
    
    @admin.display(ordering="owner__email", description="Owner Email")
    def owner_email(self, obj):
        return obj.owner.email

    @admin.display(description="Logo Preview")
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 35px; height: 35px; border-radius: 4px; object-fit: cover;" />', obj.logo.url)
        return format_html('<span style="color: #999;">No Logo</span>')

    @admin.display(description="Current Uploaded Logo")
    def display_logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 120px; border-radius: 8px;" />', obj.logo.url)
        return "No logo uploaded yet."

    @admin.action(description="Mark selected vendors as ACTIVE")
    def bulk_approve_vendors(self, request, queryset):
        updated_count = queryset.update(status=Vendor.Status.ACTIVE)
        self.message_user(
            request, 
            f"Successfully activated {updated_count} vendor storefronts.", 
            messages.SUCCESS
        )

    @admin.action(description="Mark selected vendors as SUSPENDED")
    def bulk_suspend_vendors(self, request, queryset):
        updated_count = queryset.update(status=Vendor.Status.SUSPENDED)
        self.message_user(
            request, 
            f"Successfully suspended {updated_count} vendor storefronts.", 
            messages.WARNING
        )

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", 'id',"country_code", "currency_code", "phone_prefix", "is_active")
    list_editable = ("is_active",)
    search_fields = ("name", "country_code")
    ordering = ["name"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_active")
    list_editable = ("is_active",)
    list_filter = ("country", "is_active")
    search_fields = ("name", "country__name")
    ordering = ["country", "name"]