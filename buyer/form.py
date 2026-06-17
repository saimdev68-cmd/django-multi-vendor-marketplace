from django import forms
from django.core.exceptions import ValidationError
from .models import Buyer


class BuyerForm(forms.ModelForm):
    
    phone_number = forms.CharField(
        label="Contact Phone Number (E.164 Format)",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "+1234567890",
            "class": "form-control layout-input"
        }),
        help_text="Enter your mobile number including country code (e.g., +1234567890)."
    )
    
    profile_image = forms.ImageField(
        label="Profile Avatar Image",
        required=False,
        widget=forms.FileInput(attrs={
            "class": "form-control-file layout-file-upload",
            "accept": "image/*"
        }),
        help_text="Upload a clear profile picture. Supported formats: PNG, JPG, JPEG."
    )

    class Meta:
        model = Buyer
        fields = [
            "phone_number",
            "profile_image"
        ]

    def clean_phone_number(self) -> str | None:
        """
        Pre-emptively processes phone input, stripping spaces and structural noises
        to hand a standardized, lean string down to the model layer validation.
        """
        phone = self.cleaned_data.get("phone_number")
        if not phone:
            return None
            
        # Strip internal and wrapping whitespaces
        standardized_phone = "".join(phone.split())
        return standardized_phone

    def clean(self) -> dict:
        """
        Interceptors to protect operational exceptions before hitting database blocks.
        Ensures logical and safe cohesion between related fields.
        """
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        profile_image = cleaned_data.get("profile_image")

        # Business Constraint Rule: A profile cannot be initialized completely blank.
        # At least one verified communication channel or asset must be provided.
        if not phone_number and not profile_image:
            raise ValidationError(
                "Incomplete profile update. You must provide either a valid contact "
                "phone number or upload an avatar image to update your account profiles."
            )

        return cleaned_data