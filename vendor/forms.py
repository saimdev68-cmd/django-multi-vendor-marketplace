from django import forms
from django.core.exceptions import ValidationError
from .models import Vendor

class VendorForm(forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields = [
            "store_name", 
            "description", 
            "logo", 
            "banner", 
            "phone_number", 
            "country", 
            "city", 
            "address"
        ]
        
        widgets = {
            "store_name": forms.TextInput(attrs={"placeholder": "e.g. Apex Tech Shop"}),
            "description": forms.Textarea(attrs={
                "placeholder": "Tell customers about your storefront history, brand values, or specialty products...",
                "rows": 6,
            }),
            "phone_number": forms.TextInput(attrs={"placeholder": "e.g. +923001234567"}),
            # FIX: Removed the custom "country" TextInput widget replacement entirely 
            # to let django-countries render its own secure dropdown selection.
            "city": forms.TextInput(attrs={"placeholder": "New York"}),
            "address": forms.Textarea(attrs={
                "placeholder": "Street address, suite, unit, or business office location...",
                "rows": 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Premium Minimalist Design Tokens Scale
        base_css_classes = (
            "w-full px-4 py-2.5 text-sm bg-white border border-gray-200 rounded-lg shadow-sm "
            "focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 "
            "transition-all duration-200 text-gray-800 placeholder-gray-400"
        )
        
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs.update({"class": base_css_classes})
            
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    "class": "w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 "
                             "file:rounded-md file:border-0 file:text-sm file:font-semibold "
                             "file:bg-blue-50 file:text-blue-600 hover:file:bg-blue-100 "
                             "cursor-pointer transition-colors"
                })

    def clean_store_name(self):
        store_name = self.cleaned_data.get("store_name")
        if store_name:
            store_name = store_name.strip()
            if Vendor.objects.filter(store_name__iexact=store_name).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A storefront with this name already exists. Please choose a unique name.")
        return store_name

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            max_size_bytes = 2 * 1024 * 1024 
            if logo.size > max_size_bytes:
                raise ValidationError("Store logo profile image cannot exceed 2MB in size.")
        return logo

    def clean_banner(self):
        banner = self.cleaned_data.get("banner")
        if banner:
            max_size_bytes = 5 * 1024 * 1024 
            if banner.size > max_size_bytes:
                raise ValidationError("Store banner background image cannot exceed 5MB in size.")
        return banner