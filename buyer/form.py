from django import forms
from .models import Buyer


class BuyerForm(forms.ModelForm):

    class Meta:
        model = Buyer
        fields = [
            "phone_number",
            "profile_image"
        ]