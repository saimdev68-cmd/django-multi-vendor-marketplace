from django import forms
from .models import BankAccount

class BankAccountForm(forms.ModelForm):
    
    class Meta:
        model = BankAccount
        fields = [
            "account_holder_name", 
            "bank_name", 
            "account_number", 
            "iban_number", 
            "account_type"
        ]
        
        widgets = {
            "account_holder_name": forms.TextInput(attrs={"placeholder": "e.g. Jane Doe / Company Name"}),
            "bank_name": forms.TextInput(attrs={"placeholder": "e.g. Chase, Barclays, HSBC"}),
            "account_number": forms.TextInput(attrs={"placeholder": "Enter account number digits"}),
            "iban_number": forms.TextInput(attrs={"placeholder": "e.g. GB29UKBU12345678901234"}),
            "account_type": forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_css_classes = (
            "w-full px-4 py-2.5 text-sm bg-white border border-gray-200 rounded-lg shadow-sm "
            "focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 "
            "transition-all duration-200 text-gray-800 placeholder-gray-400"
        )
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": base_css_classes})

    def clean_account_holder_name(self):
        """ Trims extra spaces and normalizes title casing for business compliance. """
        name = self.cleaned_data.get("account_holder_name")
        if name:
            return name.strip().title()
        return name

    def clean_iban_number(self):
        """ Cleans spaces and forces uppercase matching for lookups. """
        iban = self.cleaned_data.get("iban_number")
        if iban:
            return iban.replace(" ", "").upper()
        return iban

    def clean_account_number(self):
        """ Removes accidental spaces or dashes added by merchants during typing. """
        account_number = self.cleaned_data.get("account_number")
        if account_number:
            return account_number.replace(" ", "").replace("-", "").upper()
        return account_number