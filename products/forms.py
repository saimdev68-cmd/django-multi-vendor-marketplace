from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "discount_price",
            "status",
            "image",
            "stock",
        ]

        labels = {
            "name": "Product Title",
            "category": "Marketplace Category",
            "description": "Detailed Description",
            "price": "Standard Retail Price ($)",
            "discount_price": "Promotional Sale Price ($)",
            "status": "Listing Visibility Status",
            "image": "Primary Display Image",
            "stock": "Available Inventory Quantity",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select a Product Category"
        
        allowed_statuses = [
            (Product.ProductStatus.DRAFT, "Save as Draft"),
            (Product.ProductStatus.PENDING, "Submit for Review")
        ]
        
        if self.instance and self.instance.pk:
            if self.instance.status == Product.ProductStatus.ACTIVE:
                allowed_statuses.append((Product.ProductStatus.ACTIVE, "Active / Visible"))
            elif self.instance.status == Product.ProductStatus.REJECTED:
                allowed_statuses.append((Product.ProductStatus.REJECTED, "Rejected / Appeal Status"))
                
        self.fields['status'].choices = allowed_statuses

        tailwind_input_class = (
            "block w-full rounded-lg border border-slate-200/80 bg-white px-4 py-2.5 "
            "text-slate-900 placeholder-slate-400 focus:border-blue-500 focus:ring-2 "
            "focus:ring-blue-100 focus:outline-none transition-all duration-200 sm:text-sm"
        )
        
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs.update({'class': tailwind_input_class})
                
        self.fields['name'].widget.attrs['placeholder'] = "e.g., Premium Leather Messenger Bag"
        self.fields['price'].widget.attrs['placeholder'] = "0.00"
        self.fields['discount_price'].widget.attrs['placeholder'] = "0.00 (Optional)"
        self.fields['stock'].widget.attrs['placeholder'] = "0"
        self.fields['description'].widget.attrs['rows'] = "4"
        self.fields['description'].widget.attrs['placeholder'] = "Provide a detailed overview of your product features..."
        
        self.fields['image'].widget.attrs['class'] = (
            "block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 "
            "file:rounded-md file:border-0 file:text-sm file:font-semibold "
            "file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100 transition-all cursor-pointer"
        )

    def clean(self):

        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        discount_price = cleaned_data.get("discount_price")
        status = cleaned_data.get("status")
        image = cleaned_data.get("image")

        if discount_price and price and discount_price >= price:
            self.add_error(
                "discount_price",
                ValidationError("The discount promotional price must be strictly less than the regular retail price.")
            )

        if status == Product.ProductStatus.ACTIVE and not image and not (self.instance and self.instance.image):
            self.add_error(
                "image",
                ValidationError("An active product catalog listing must have a valid display image uploaded.")
            )

        return cleaned_data