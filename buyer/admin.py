from django.contrib import admin
from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):

    list_display = ("user",'id',"phone_number")
    search_fields = ("user__email","phone_number")
    readonly_fields = ("created_at","updated_at")

    fieldsets = (
        ("User Info", {
            "fields": ("user",)
        }),
        ("Profile Info", {
            "fields": (
                "phone_number",
                "profile_image",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )