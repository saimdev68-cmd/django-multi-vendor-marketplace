import os
from decimal import Decimal
from django.db import models 
from accounts.models import User 
from django.utils.text import slugify
from django.core.validators import MinValueValidator , MaxValueValidator , RegexValidator
from django_countries.fields import CountryField
from .managers import VendorManager


def vendor_media_path(instance,filename):
    ext = filename.split(".")[-1]
    folder_slug = instance.slug if instance.slug else slugify(instance.store_name)
    return os.path.join('vendor',folder_slug,f"logo.{ext}")

def vendor_banner_path(instance,filename):
    ext = filename.split('.')[-1]
    folder_slug = instance.slug if instance.slug else slugify(instance.store_name)
    return os.path.join('vendor',folder_slug,f"banner.{ext}")

class Vendor(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        REJECTED = "rejected", "Rejected"

    phone_validation = RegexValidator(
        regex=r'^\+?[1-9]\d{8,14}$',
        message="Enter a valid phone number including country code (e.g., +923001234567 or 923001234567)."
    )

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor")

    store_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,editable=False)
    description = models.TextField(blank=True)

    logo = models.ImageField(upload_to=vendor_media_path, blank=True, null=True)
    banner = models.ImageField(upload_to=vendor_banner_path, blank=True, null=True)

    phone_number = models.CharField(max_length=17,unique=True,null=True,blank=True,validators=[phone_validation])
    country = CountryField()
    city = models.CharField(max_length=100)
    address = models.TextField()

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING,db_index=True)
    is_featured = models.BooleanField(default=False,db_index=True)

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

    def __str__(self):
        return self.store_name
    
    @property
    def get_full_address(self):
        return f"{self.address}, {self.city} , {self.country}"