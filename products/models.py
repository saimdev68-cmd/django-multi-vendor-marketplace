from django.db import models
from django.utils.text import slugify
from vendor.models import Vendor
import os
from django.core.validators import MinValueValidator 
from django.core.exceptions import ValidationError
from decimal import Decimal
import uuid

def category_image_path(instance,filename):
    ext = filename.split('.')[-1]
    slug_folder = instance.slug if instance.slug else slugify(instance.name)
    return os.path.join('category',slug_folder,f'icon.{ext}')

def product_image_path(instance,filename):
    ext = filename.split('.')[-1]
    unique_seed = uuid.uuid4().hex[:10]
    vendor_path = str(instance.vendor_id)
    return os.path.join('products',vendor_path,f"img_{unique_seed}.{ext}")

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    icon = models.ImageField(upload_to=category_image_path,null=True,blank=True)
    is_active = models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
class Product(models.Model):

    class ProductStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        OUT_OF_STOCK = "out_of_stock", "Out of Stock"
        REJECTED = "rejected", "Rejected"

    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name="products")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="products")

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    sku = models.CharField(
        max_length=64, 
        unique=True, 
        blank=True,
        db_index=True,
        help_text="Stock Keeping Unit for inventory tracking. Must be globally unique."
    )
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    discount_price = models.DecimalField(
        max_digits=10,decimal_places=2,
        null=True,blank=True,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20,choices=ProductStatus.choices,default=ProductStatus.DRAFT)
    is_featured = models.BooleanField(default=False,db_index=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['status','category','-created_at']),
            models.Index(fields=['status','is_featured','-created_at']),
            models.Index(fields=['vendor','status'])
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price


    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug or self.name != self.__original_name:
            base = slugify(self.name)
            short_hash = uuid.uuid4().hex[:6]
            self.slug = f"{base}-{short_hash}"

        if not self.sku:
            vendor_prefix = f"VND{self.vendor_id:04d}"
            category_prefix = f"CAT{self.category_id:03d}" if self.category_id else "CAT000"
            random_suffix = uuid.uuid4().hex[:6].upper()
            
            generated_sku = f"{vendor_prefix}-{category_prefix}-{random_suffix}"
            while Product.objects.filter(sku=generated_sku).exists():
                random_suffix = uuid.uuid4().hex[:6].upper()
                generated_sku = f"{vendor_prefix}-{category_prefix}-{random_suffix}"
                
            self.sku = generated_sku
        super().save(*args, **kwargs)
        self.__original_name = self.name