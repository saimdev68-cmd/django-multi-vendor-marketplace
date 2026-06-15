from django.utils.text import slugify
from vendor.models import Vendor
from django.db import IntegrityError
 
class VendorService:

    @staticmethod
    def generate_unique_slug(store_name):
        base_slug = slugify(store_name)
        slug = base_slug
        counter = 1

        while Vendor.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    @staticmethod
    def create_vendor(user, **data):
        data["owner"] = user
        data["slug"] = VendorService.generate_unique_slug(data["store_name"])
        try:
            return Vendor.objects.create(**data)
        except IntegrityError:
            data["slug"] = VendorService.generate_unique_slug(data["store_name"])
            return Vendor.objects.create(**data)