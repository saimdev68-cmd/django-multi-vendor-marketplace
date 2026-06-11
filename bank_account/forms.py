from django import forms
from .models import  BankAccount

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["account_holder_name", "bank_name", "account_number", "iban_number", "account_type"]