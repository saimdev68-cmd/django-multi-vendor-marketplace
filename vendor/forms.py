from django import forms
from .models import Vendor

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["store_name", "description", "logo", "banner", "phone_number", "country", "city", "address"]
    
