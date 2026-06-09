from django.contrib import admin
from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone_number",
        "gender",
        "is_verified",
        "created_at",
    )

    list_filter = (
        "gender",
        "is_verified",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "phone_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("User Info", {
            "fields": ("user",)
        }),
        ("Profile Info", {
            "fields": (
                "phone_number",
                "profile_image",
                "date_of_birth",
                "gender",
            )
        }),
        ("Address Info", {
            "fields": (
                "address",
            )
        }),
        ("Verification", {
            "fields": (
                "is_verified",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )