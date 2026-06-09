from django.db import models
from django.utils.text import slugify
from vendor.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.id}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):

    class ProductStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        OUT_OF_STOCK = "out_of_stock", "Out of Stock"
        ARCHIVED = "archived", "Archived"

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=ProductStatus.choices,
        default=ProductStatus.DRAFT
    )
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            # Get all slugs starting with same base
            existing_slugs = self.__class__.objects.filter(slug__startswith=base_slug)

            # Extract numbers from similar slugs
            slugs = existing_slugs.values_list("slug", flat=True)

            counter = 1
            while slug in slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price