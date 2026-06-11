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

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor")

    store_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to="vendors/logos/", blank=True, null=True)
    banner = models.ImageField(upload_to="vendors/banners/", blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    status = models.CharField(max_length=20,choices=VendorStatus.choices,default=VendorStatus.PENDING)
    is_featured = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5,decimal_places=2,default=10.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.store_name

    def get_full_address(self):
        return f"{self.address}, {self.city} , {self.country}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.store_name)
            slug = base_slug
            counter = 1
            while Vendor.objects.filter(slug=slug).exclude():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
