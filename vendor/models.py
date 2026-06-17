from decimal import Decimal

from django.db import models 
from accounts.models import User 
from store.models import Country , City , Currency , Bank

from django.utils.text import slugify
from django.core.validators import MinValueValidator , MaxValueValidator , RegexValidator
from django.core.exceptions import ValidationError

from .managers import VendorManager


def vendor_media_path(instance, filename):
    ext = filename.split(".")[-1]
    folder_slug = instance.slug if instance.slug else slugify(instance.name)
    return f"vendor/{folder_slug}/logo.{ext}"

def vendor_banner_path(instance, filename):
    ext = filename.split('.')[-1]
    folder_slug = instance.slug if instance.slug else slugify(instance.name)
    return f"vendor/{folder_slug}/banner.{ext}"

class Vendor(models.Model):

    class Status(models.TextChoices):

        PENDING_APPROVAL = "pending_approval", "Pending Admin Review"
        INCOMPLETE_PROFILE = "incomplete_profile", "Incomplete Setup (Missing Info/Bank)"
        REJECTED = "rejected", "Application Rejected"
        
        ACTIVE = "active", "Active & Operational"
        MAINTENANCE = "maintenance", "On Vacation / Temporarily Paused"

        SUSPENDED = "suspended", "Suspended (Policy Violation)"
        RESTRICTED = "restricted", "Restricted (Payouts Blocked / Under Review)"

        TERMINATED = "terminated", "Account Closed / Contract Ended"

    phone_validation = RegexValidator(
        regex=r'^\+?[1-9]\d{8,14}$',
        message="Enter a valid phone number including country code (e.g., +923001234567 or 923001234567)."
    )

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor")

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField()

    logo = models.ImageField(upload_to=vendor_media_path,null=True,blank=True)
    banner = models.ImageField(upload_to=vendor_banner_path,null=True,blank=True)

    phone = models.CharField(max_length=17 , unique=True, validators=[phone_validation])
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True , related_name="vendors")
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True , related_name="vendors")
    address = models.TextField()

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING_APPROVAL,db_index=True)
    is_featured = models.BooleanField(default=False,db_index=True)

    is_verified = models.BooleanField(default=False, db_index=True, help_text="Designates whether this vendor passed legal background verification.")
    tax_identifier = models.CharField(max_length=100, blank=True, null=True, help_text="Business tax registration, VAT, or EIN number.")
    status_notes = models.TextField(blank=True, help_text="Internal notes explaining rejections or suspensions.")

    commission_rate = models.DecimalField(
        max_digits=5,decimal_places=2,default=Decimal('10.00'),
        validators=[MinValueValidator(Decimal('0.00')) , MaxValueValidator(Decimal('30.00'))],
        help_text="Vendor-specific commission percentage.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VendorManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "vendor"
        verbose_name_plural = "Vendors"
        db_table = 'vendors'
        indexes = [
            models.Index(fields=["status","-created_at"]),
            models.Index(fields=["is_featured","status"]),
            models.Index(fields=["country",'city'])
        ]

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        if self.city and self.country and self.city.country != self.country:
            raise ValidationError({"city": "The selected city does not belong to the selected country."})
    
    @property
    def get_full_address(self):
        return f"{self.address},{self.city.name},{self.country.name}"
    
class BankAccount(models.Model):

    class Type(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    class Status(models.TextChoices):

        INCOMPLETE = "incomplete", "Incomplete Setup (Missing Info)"
        PENDING = "pending", "Pending Verification"
        
        VERIFYING = "verifying", "Verification In Progress (Micro-deposits Sent)"
        VERIFIED = "verified", "Verified & Active"
        
        REJECTED = "rejected", "Rejected (Invalid Details)"
        SUSPENDED = "suspended", "Payouts Frozen / Blocked by Admin"

    swift_validator = RegexValidator(
        regex=r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$",
        message="Invalid SWIFT/BIC format. Must be a valid 8 or 11 character banking identifier."
    )

    alphanumeric_validator = RegexValidator(
        regex=r'^[A-Z0-9]{5,50}$',
        message="Must contain only uppercase letters and digits, between 5 and 50 characters."
    )

    vendor = models.OneToOneField(Vendor,on_delete=models.CASCADE,related_name="bank")

    bank_name = models.ForeignKey(Bank,on_delete=models.SET_NULL,null=True)
    swift_bic = models.CharField(max_length=11,validators=[swift_validator],help_text="BIC/SWIFT code for international routing.")
    currency = models.ForeignKey(Currency,on_delete=models.SET_NULL,null=True)

    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50,validators=[alphanumeric_validator])
    iban_number = models.CharField(max_length=50,unique=True,validators=[alphanumeric_validator])
    account_type = models.CharField(max_length=20,choices=Type.choices,default=Type.CURRENT)

    status = models.CharField(max_length=20,choices=Status,default=Status.PENDING)
    status_notes = models.TextField(blank=True, help_text="Internal notes explaining rejections or suspensions.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
        db_table = 'bank_accounts'
        indexes = [
            models.Index(fields=['status','-created_at']),
            models.Index(fields=['currency','status'])
        ]

    def __str__(self):
        return f"{self.bank_name} - {self.account_holder_name}"
    
class VendorStatusLog(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="status_logs")
    changed_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,
        help_text="The administrative user or operator who triggered this status modification change event."
    )
    old_status = models.CharField(max_length=25, choices=Vendor.Status.choices, null=True, blank=True)
    new_status = models.CharField(max_length=25, choices=Vendor.Status.choices)
    reason = models.TextField(blank=True, help_text="Reason or notes regarding this status change.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendor_status_logs'
        ordering = ["-created_at"]

    def __str__(self):
        return f"Vendor: {self.vendor.name} | {self.old_status} ➔ {self.new_status}"


class BankAccountStatusLog(models.Model):

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="status_logs")
    changed_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,
        help_text="The administrative user or operator who triggered this status modification change event."
    )
    old_status = models.CharField(max_length=25, choices=BankAccount.Status.choices, null=True, blank=True)
    new_status = models.CharField(max_length=25, choices=BankAccount.Status.choices)
    reason = models.TextField(blank=True, help_text="Reason or notes regarding this status change.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bank_account_status_logs'
        ordering = ["-created_at"]

    def __str__(self):
        return f"Bank Acc ID: {self.bank_account.id} | {self.old_status} ➔ {self.new_status}"