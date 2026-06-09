from django.db import models
from django.utils import timezone
from accounts.models import User
from django.utils.text import slugify


class Vendor(models.Model):

    class VendorStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        REJECTED = "rejected", "Rejected"

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vendor"
    )

    store_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="vendors/logos/", blank=True, null=True)
    banner = models.ImageField(upload_to="vendors/banners/", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=VendorStatus.choices,
        default=VendorStatus.PENDING
    )
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5,decimal_places=2,default=10.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.store_name

    def get_full_address(self):
        return f"{self.address}, {self.city}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = f"{self.store_name}-{self.id or ''}"
            self.slug = slugify(base_slug).strip("-")
        super().save(*args, **kwargs)
    

class BankAccount(models.Model):

    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    vendor = models.OneToOneField(
        Vendor,
        on_delete=models.CASCADE,
        related_name="bank_account"
    )

    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    iban_number = models.CharField(max_length=50, blank=True, null=True)
    swift_code = models.CharField(max_length=20, blank=True, null=True)

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.CURRENT
    )

    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.bank_name} - {self.account_holder_name}"