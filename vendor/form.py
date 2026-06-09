from django import forms
from .models import Vendor, BankAccount

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["store_name", "description", "logo", "banner", "phone_number", "city", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through fields to dynamically inject styling attributes
        for field_name, field in self.fields.items():
            if field_name == "description":
                field.widget.attrs.update({'rows': 3, 'placeholder': 'Tell buyers about your shop...'})
            elif field_name in ["logo", "banner"]:
                # Custom adjustments for files can go here if needed
                pass
            else:
                field.widget.attrs.update({'placeholder': f'Enter {field_name.replace("_", " ")}'})


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["account_holder_name", "bank_name", "account_number", "iban_number", "swift_code", "account_type", "is_primary"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_primary':
                field.widget.attrs.update({'placeholder': f'Enter {field_name.replace("_", " ")}'})