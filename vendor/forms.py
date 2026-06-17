from django import forms
from django.core.exceptions import ValidationError
from .models import Vendor , BankAccount
from store.models import Country , City , Currency , Bank

class VendorForm(forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields = [
            "name", 
            "description", 
            "logo", 
            "banner", 
            "phone", 
            "country", 
            "city", 
            "address",
            'tax_identifier'
        ]

        labels = {
            "name": "Legal Business Name",
            "description": "Storefront Description",
            "logo": "Brand Logo (Profile)",
            "banner": "Storefront Cover Banner",
            "phone": "Business Contact Number",
            "country": "Operating Country",
            "city": "Operating City",
            "address": "Complete Business Address",
            "tax_identifier": "Corporate Tax Registration ID",
        }

        help_text = {
            "logo": "Upload a square brand avatar (PNG or JPG). File size cap: 2MB.",
            "banner": "A high-resolution widescreen layout backdrop for your marketplace landing page. Max size: 5MB.",
        }
        
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. TrendHub Store"}),
            "description": forms.Textarea(attrs={
                "placeholder": "Tell customers about your storefront history, brand values, or specialty products...",
                "rows": 6,
            }),
            "phone": forms.TextInput(attrs={"placeholder": "e.g. +923001234567"}),
            "country": forms.Select(),
            "city": forms.Select(),
            "address": forms.Textarea(attrs={
                "placeholder": "Street address, suite, unit, or business office location...",
                "rows": 4,
            }),
            "tax_identifier": forms.TextInput(attrs={
            "placeholder": "e.g. TRN-7654321, NTN, or VAT ID..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["country"].queryset = Country.objects.filter(is_active=True)
        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["city"].queryset = City.objects.filter(
                    country_id=country_id, 
                    is_active=True
                ).select_related("country")
            except (ValueError, TypeError):
                self.fields["city"].queryset = City.objects.none()
                
        elif self.instance.pk and self.instance.country:
            self.fields["city"].queryset = self.instance.country.cities.filter(
                is_active=True
            ).select_related("country")
        else:
            self.fields["city"].queryset = City.objects.none()  
        
        base_css_classes = (
            "w-full px-4 py-2.5 text-sm bg-white border border-gray-200 rounded-lg shadow-sm "
            "focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 "
            "transition-all duration-200 text-gray-800 placeholder-gray-400 cursor-pointer"
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

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name = name.strip()
            if Vendor.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A storefront with this name already exists. Please choose a unique name.")
        return name

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
    
class BankAccountForm(forms.ModelForm):
    
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        empty_label="Select Settlement Currency",
        label="Settlement Currency",
        required=True
    )

    bank_name = forms.ModelChoiceField(
        queryset=Bank.objects.filter(is_active=True),
        required=True
    )

    class Meta:
        model = BankAccount
        fields = [
            "account_holder_name", 
            "bank_name", 
            "swift_bic", 
            "currency",
            "account_number", 
            "iban_number", 
            "account_type"
        ]
        
        labels = {
            "account_holder_name": "Account Holder Name",
            "bank_name": "Financial Institution Name",
            "swift_bix": "SWIFT / BIC Code",
            "account_number": "Account Number",
            "iban_number": "International Bank Account Number (IBAN)",
            "account_type": "Account Type Classification"
        }
        
        widgets = {
            "account_holder_name": forms.TextInput(attrs={"placeholder": "e.g. Jane Doe / Company Name"}),
            "bank_name": forms.Select(),
            "swift_bix": forms.TextInput(attrs={"placeholder": "e.g. KCBAUS33XXX"}),
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
        
        name = self.cleaned_data.get("account_holder_name")
        if name:
            return name.strip().title()
        return name

    def clean_swift_bix(self):
        
        swift = self.cleaned_data.get("swift_bix")
        if swift:
            return swift.replace(" ", "").upper()
        return swift

    def clean_iban_number(self):
       
        iban = self.cleaned_data.get("iban_number")
        if iban:
            return iban.replace(" ", "").upper()
        return iban

    def clean_account_number(self):
        
        account_number = self.cleaned_data.get("account_number")
        if account_number:
            return account_number.replace(" ", "").replace("-", "").upper()
        return account_number