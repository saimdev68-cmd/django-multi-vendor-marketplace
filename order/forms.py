from django import forms
from vendor.models import Country, City
from .models import Order


class OrderCheckoutForm(forms.ModelForm):
    """
    Defensive form perimeter for collecting structured customer delivery data.
    Integrates clean model choices for relational country and city targets.
    """
    name = forms.CharField(
        label="Recipient Full Name",
        widget=forms.TextInput(attrs={
            "placeholder": "John Doe",
            "class": "form-control checkout-input"
        })
    )
    phone_number = forms.CharField(
        label="Contact Phone Number",
        widget=forms.TextInput(attrs={
            "placeholder": "+1234567890",
            "class": "form-control checkout-input"
        })
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label="Country",
        empty_label="Select your country",
        widget=forms.Select(attrs={
            "class": "form-control checkout-select"
        })
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.none(),  # Populated via AJAX on frontend or initialized cleanly
        label="City / Region",
        empty_label="Select your city",
        widget=forms.Select(attrs={
            "class": "form-control checkout-select"
        })
    )
    shipping_address = forms.CharField(
        label="Street Address",
        widget=forms.Textarea(attrs={
            "placeholder": "123 Market Place, Apt 4B",
            "class": "form-control checkout-textarea",
            "rows": 3
        })
    )

    class Meta:
        model = Order
        fields = [
            "name",
            "phone_number",
            "country",
            "city",
            "shipping_address",
        ]

    def __init__(self, *args, **kwargs):
        """
        Dynamically filters the city queryset based on the submitted country 
        to guarantee database integrity during raw post submissions.
        """
        super().__init__(*args, **kwargs)
        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["city"].queryset = City.objects.filter(country_id=country_id)
            except (ValueError, TypeError):
                pass  # Fallback to empty if form data is corrupted
        elif self.instance.pk and self.instance.country:
            self.fields["city"].queryset = self.instance.country.cities.all()
        else:
            self.fields["city"].queryset = City.objects.all()  # Safe fallback for basic layout renders