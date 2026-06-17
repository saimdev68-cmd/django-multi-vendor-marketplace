from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    # --- Performance Optimization ---
    # Strictly eradicates N+1 loops by eagerly loading the related User model in a single JOIN
    list_select_related = ("user",)

    # --- UI & Layout Configuration ---
    list_display = (
        "id",
        "get_user_email",
        "phone_number",
        "created_at",
    )
    list_display_links = ("id", "get_user_email")
    list_filter = ("created_at",)
    search_fields = ("user__email", "phone_number")
    
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("User Authentication", {
            "fields": ("user",),
            "description": "Core account mapping linking this profile to authenticated credentials."
        }),
        ("Profile Data", {
            "fields": (
                "phone_number",
                "profile_image",
            )
        }),
        ("System Metadata", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",)  # Keeps advanced data hidden unless expanded by an admin
        }),
    )

    # --- Custom Column Methods ---
    @admin.display(ordering="user__email", description="User Email")
    def get_user_email(self, obj: Buyer) -> str:
        """Accesses the related user email cleanly without triggering extra SQL."""
        return obj.user.email

    # --- Bulk Operational Actions ---
    actions = ["clear_profile_images"]

    @admin.action(description="Reset selected profile images to system default")
    def clear_profile_images(self, request: HttpRequest, queryset: QuerySet) -> None:
        """
        Bulk administrative utility to sanitize profile imagery en masse.
        Delegates file sweeps directly to django-cleanup under the hood on update.
        """
        updated_count = queryset.update(profile_image="buyers/profiles/default.png")
        self.message_user(
            request,
            f"Successfully reset the profile image for {updated_count} buyer accounts.",
            messages.SUCCESS
        )