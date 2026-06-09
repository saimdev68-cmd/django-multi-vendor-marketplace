from django import forms
from .models import Buyer


class BuyerForm(forms.ModelForm):

    class Meta:
        model = Buyer
        fields = [
            "phone_number",
            "profile_image",
            "date_of_birth",
            "gender",
            "address",
        ]

        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }