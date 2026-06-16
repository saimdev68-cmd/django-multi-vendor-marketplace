from decimal import Decimal
from django.db import models 
from accounts.models import User 
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

class Country(models.Model):

    name = models.CharField(max_length=200 , unique=True)
    country_code = models.CharField(max_length=10 , unique=True)
    currency_code = models.CharField(max_length=3, default="USD", help_text="ISO currency code (e.g., USD, EUR)")
    phone_prefix = models.CharField(max_length=7, blank=True, help_text="International phone prefix (e.g., +1 or +92)")
    is_active = models.BooleanField(default=True ,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]
        db_table = "countries"

    def __str__(self):
        return self.name
    
class City(models.Model):

    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="cities")

    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True , db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name},{self.country.name}"
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = ("country",'name')
        ordering = ["name"]
        db_table = "cities"
        indexes = [ 
            models.Index(fields=["country",'is_active'])
        ]
    

class Vendor(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REJECTED = "rejected", "Rejected"
        ACTIVE = "active", "Active"
        SUSPENDED = "suspended", "Suspended"

    phone_validation = RegexValidator(
        regex=r'^\+?[1-9]\d{8,14}$',
        message="Enter a valid phone number including country code (e.g., +923001234567 or 923001234567)."
    )

    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="vendor")

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(blank=True)

    logo = models.ImageField(upload_to=vendor_media_path, blank=True, null=True)
    banner = models.ImageField(upload_to=vendor_banner_path, blank=True, null=True)

    phone = models.CharField(max_length=17,unique=True,null=True,blank=True,validators=[phone_validation])
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True , related_name="vendors")
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True , related_name="vendors")
    address = models.TextField()

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING,db_index=True)
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
        parts = [self.address]
        if self.city:
            parts.append(self.city.name)
        if self.country:
            parts.append(self.country.name)
        return ", ".join(p for p in parts)