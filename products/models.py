import uuid
from django.db import models
from django.utils.text import slugify
from vendor.models import Vendor
from django.core.validators import MinValueValidator 
from django.core.exceptions import ValidationError
from decimal import Decimal

def product_image_path(instance,filename):
    ext = filename.split('.')[-1].lower()
    unique_seed = uuid.uuid4().hex[:10]
    vendor_id = str(instance.vendor_id) if instance.vendor_id else "0"
    return f"products/vendor_{vendor_id}/{unique_seed}.{ext}"

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True,blank=True)
    icon = models.ImageField(upload_to="Category/",null=True,blank=True)
    is_active = models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"
        ordering = ["-created_at"]
        db_table = 'categories'

    def __str__(self):
        return self.name
    
class Product(models.Model):

    class ProductStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending","Pending"
        ACTIVE = "active", "Active"
        REJECTED = "rejected", "Rejected"

    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name="products")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="products")

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    sku = models.CharField(
        max_length=64, 
        unique=True, 
        blank=True,
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
    is_featured = models.BooleanField(default=False, db_index=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
        db_table = 'products'
        indexes = [
            models.Index(fields=['status','category','-created_at']),
            models.Index(fields=['status','is_featured','-created_at']),
            models.Index(fields=['vendor','status'])
        ]
    
    def __str__(self):
        return self.name

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def clean(self):
        super().clean()
        if self.discount_price and self.discount_price >= self.price:
            raise ValidationError({'discount_price': "Discount price must be strictly less than the standard price."})
            
        if self.status == self.ProductStatus.ACTIVE and not self.image:
            raise ValidationError({'image': "An active product catalog listing must have a valid display image uploaded."})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)