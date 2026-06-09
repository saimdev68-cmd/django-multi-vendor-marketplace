from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    # Explicitly declaring the additional image fields to support your multi-angle preview slots
    image_2 = forms.ImageField(
        required=False,
        label="Showcase Angle 2",
        widget=forms.ClearableFileInput(attrs={'class': 'hidden-file-input'})
    )
    image_3 = forms.ImageField(
        required=False,
        label="Detail View",
        widget=forms.ClearableFileInput(attrs={'class': 'hidden-file-input'})
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "discount_price",
            "stock",
            "sku",
            "status",
            "image",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "e.g., Wireless Mechanical Keyboard Pro",
                "class": "form-control"
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Tell buyers about the premium features, materials, and specifications...",
                "rows": 4,
                "class": "form-control"
            }),
            "price": forms.NumberInput(attrs={
                "placeholder": "0.00",
                "min": "0.00",
                "step": "0.01",
                "class": "form-control"
            }),
            "discount_price": forms.NumberInput(attrs={
                "placeholder": "0.00 (Optional)",
                "min": "0.00",
                "step": "0.01",
                "class": "form-control"
            }),
            "stock": forms.NumberInput(attrs={
                "placeholder": "Available quantity",
                "min": "0",
                "class": "form-control"
            }),
            "sku": forms.TextInput(attrs={
                "placeholder": "MKTL-XXXX-XXXX",
                "class": "form-control"
            }),
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "hidden-file-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Iterates over all form widgets to apply core interactive structural styles automatically
        for field_name, field in self.fields.items():
            # Keeps our file inputs clean for the custom JavaScript preview loops
            if 'hidden-file-input' not in field.widget.attrs.get('class', ''):
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-3 focus:ring-blue-100 transition-all bg-white text-slate-900 shadow-sm'
                })

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Marketly products cannot carry a negative base value.")
        return price

    def clean_discount_price(self):
        price = self.cleaned_data.get('price')
        discount_price = self.cleaned_data.get('discount_price')
        
        if discount_price and price and discount_price >= price:
            raise forms.ValidationError("The promotional discount price must be lower than the base platform price.")
        return discount_price

    def clean_sku(self):
        sku = self.cleaned_data.get('sku', '').upper()
        # Custom cleaning to force standardization across vendor item sets
        return sku