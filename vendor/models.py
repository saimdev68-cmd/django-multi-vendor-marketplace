import os
from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.core.validators import RegexValidator , MinValueValidator , MaxValueValidator

def vendor_media_path(instance,filename):
    ext = filename.split(".")[-1]
    folder_slug = instance.slug if instance.slug else slugify(instance.store_name)
    return os.path.join('vendor',folder_slug,f"logo.{ext}")

def vendor_banner_path(instance,filename):
    ext = filename.split('.')[-1]
    folder_slug = instance.slug if instance.slug else slugify(instance.store_name)
    return os.path.join('vendor',folder_slug,f"banner.{ext}")

class Vendor(models.Model):

    class VendorStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"
        REJECTED = "rejected", "Rejected"

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor")

    store_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to=vendor_media_path, blank=True, null=True)
    banner = models.ImageField(upload_to=vendor_banner_path, blank=True, null=True)
    phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex],max_length=17,blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=20,choices=VendorStatus.choices,default=VendorStatus.PENDING,db_index=True)
    is_featured = models.BooleanField(default=False,db_index=True)
    commission_rate = models.DecimalField(
        max_digits=5,decimal_places=2,default=10.00,
        validators=[MinValueValidator(0.00) , MaxValueValidator(30.00)],
        help_text="Platform commission percentage for this specific vendor."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.store_name

    def get_full_address(self):
        return f"{self.address}, {self.city} , {self.country}"
    
    def save(self, *args, **kwargs):
        if self.pk:
            original_record = Vendor.objects.get(id=self.pk)
            if original_record.store_name != self.store_name:
                self.slug = None

        if not self.slug:
            base_slug = slugify(self.store_name)
            slug = base_slug
            counter = 1
            while Vendor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)