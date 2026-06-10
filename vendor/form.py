from django import forms
from .models import Vendor, BankAccount

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ["store_name", "description", "logo", "banner", "phone_number", "country", "city", "address"]
    

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["account_holder_name", "bank_name", "account_number", "iban_number", "account_type"]