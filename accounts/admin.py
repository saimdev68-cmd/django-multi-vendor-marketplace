from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("email","id","is_vendor","is_verified","is_staff","is_active",)

    list_filter = ("is_vendor","is_verified","is_staff","is_active","is_superuser",)

    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": (
                "is_vendor",
                "is_verified",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {"fields": ("last_login", "date_joined","updated_at")}),
    )

    readonly_fields = ("updated_at",)

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_vendor",
                "is_verified",
                "is_staff",
                "is_active",
            ),
        }),
    )