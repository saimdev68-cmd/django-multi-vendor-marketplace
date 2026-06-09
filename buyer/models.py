from django.db import models
from accounts.models import User


class Buyer(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="buyer"
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    profile_image = models.ImageField(
        upload_to="buyers/profiles/",
        default="default.png"
    )

    date_of_birth = models.DateField(blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        blank=True,
        null=True
    )
    address = models.TextField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.user.username