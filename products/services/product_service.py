import uuid
from django.utils.text import slugify
from django.db import transaction
from products.models import Product


class ProductService:

    @staticmethod
    def generate_unique_slug(product):

        if product.slug:
            return product.slug

        base_slug = slugify(product.name)
        if not base_slug:
            base_slug = "product"

        short_hash = uuid.uuid4().hex[:6].lower()
        generated_slug = f"{base_slug}-{short_hash}"

        iteration = 1
        queryset = Product.objects.all()
        if product.pk:
            queryset = queryset.exclude(pk=product.pk)

        while queryset.filter(slug=generated_slug).exists():
            short_hash = uuid.uuid4().hex[:6].lower()
            generated_slug = f"{base_slug}-{short_hash}-{iteration}"
            iteration += 1

        return generated_slug

    @staticmethod
    def generate_unique_sku(product):

        if product.sku:
            return product.sku

        vendor_prefix = f"VND{product.vendor_id:04d}" if product.vendor_id else "VND0000"
        category_prefix = f"CAT{product.category_id:03d}" if product.category_id else "CAT000"
        random_suffix = uuid.uuid4().hex[:6].upper()
        
        generated_sku = f"{vendor_prefix}-{category_prefix}-{random_suffix}"
        
        queryset = Product.objects.all()
        if product.pk:
            queryset = queryset.exclude(pk=product.pk)

        while queryset.filter(sku=generated_sku).exists():
            random_suffix = uuid.uuid4().hex[:6].upper()
            generated_sku = f"{vendor_prefix}-{category_prefix}-{random_suffix}"
            
        return generated_sku

    @classmethod
    @transaction.atomic
    def create_product_service(cls, vendor, cleaned_data, image_file=None):

        product = Product(
            vendor=vendor,
            category=cleaned_data.get('category'),
            name=cleaned_data.get('name'),
            description=cleaned_data.get('description'),
            price=cleaned_data.get('price'),
            discount_price=cleaned_data.get('discount_price'),
            stock=cleaned_data.get('stock',0),
            status=cleaned_data.get('status',Product.ProductStatus.DRAFT),
            is_featured=cleaned_data.get('is_featured',False),
            image=image_file or cleaned_data.get('image')
        )

        product.slug = cls.generate_unique_slug(product)
        product.sku = cls.generate_unique_sku(product)

        product.full_clean()
        product.save()
        
        return product
        