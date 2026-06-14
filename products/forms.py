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
            "stock",
            "status",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        # Extract custom vendor initialization constraints if passed down from views
        self.vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        
        # 1. Performance Optimization: Limit category selections to active categories only
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select a Product Category"
        
        # 2. Security Optimization: Prevent sellers from assigning unauthorized states
        allowed_statuses = [
            (Product.ProductStatus.DRAFT, "Save as Draft"),
            (Product.ProductStatus.OUT_OF_STOCK, "Mark Out of Stock")
        ]
        
        # If the instance already exists and was approved, let them maintain or toggle state cleanly
        if self.instance and self.instance.pk:
            if self.instance.status == Product.ProductStatus.ACTIVE:
                allowed_statuses.append((Product.ProductStatus.ACTIVE, "Active / Visible"))
            elif self.instance.status == Product.ProductStatus.REJECTED:
                allowed_statuses.append((Product.ProductStatus.REJECTED, "Rejected / Appeal Status"))
                
        self.fields['status'].choices = allowed_statuses

        # 3. Design System Integration: Apply pristine minimalist SaaS utility styles
        tailwind_input_class = (
            "block w-full rounded-lg border border-slate-200/80 bg-white px-4 py-2.5 "
            "text-slate-900 placeholder-slate-400 focus:border-blue-500 focus:ring-2 "
            "focus:ring-blue-100 focus:outline-none transition-all duration-200 sm:text-sm"
        )
        
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs.update({'class': tailwind_input_class})
                
        # Tailored Placeholders
        self.fields['name'].widget.attrs['placeholder'] = "e.g., Premium Leather Messenger Bag"
        self.fields['price'].widget.attrs['placeholder'] = "0.00"
        self.fields['discount_price'].widget.attrs['placeholder'] = "0.00 (Optional)"
        self.fields['stock'].widget.attrs['placeholder'] = "0"
        self.fields['description'].widget.attrs['rows'] = "4"
        self.fields['description'].widget.attrs['placeholder'] = "Provide a detailed overview of your product features..."
        
        # Custom file upload chip styles
        self.fields['image'].widget.attrs['class'] = (
            "block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 "
            "file:rounded-md file:border-0 file:text-sm file:font-semibold "
            "file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100 transition-all cursor-pointer"
        )

    def clean(self):
        """
        Defensive Form-Level validation processing.
        Transforms database exceptions into actionable UI input error tags.
        """
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        discount_price = cleaned_data.get("discount_price")

        # Early check validation gate matching our backend model constraints
        if discount_price and price and discount_price >= price:
            self.add_error(
                "discount_price",
                ValidationError("The discount promotional price must be strictly less than the regular retail price.")
            )

        return cleaned_data
    
    def clean_sku(self):
        """
        Validates and normalizes the Stock Keeping Unit (SKU).
        Transforms empty inputs to None to ensure unique database constraints 
        don't collide before the model's auto-generation engine runs.
        """
        # Use .get() defensively to avoid KeyError exceptions if 'sku' is excluded from fields
        sku = self.cleaned_data.get("sku")
        
        if sku:
            sku = sku.strip().upper()
            
            # Defensive Security Check: Ensure the user isn't trying to claim an existing SKU
            queryset = Product.objects.filter(sku=sku)
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
                
            if queryset.exists():
                raise forms.ValidationError(
                    "This SKU is already assigned to another product in the Marketly network."
                )
        else:
            # Force empty strings to None so the model's save() loop handles auto-generation safely
            sku = None
            
        return sku
    