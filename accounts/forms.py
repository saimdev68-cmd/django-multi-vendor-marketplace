from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "password1", "password2", "is_vendor"]

        labels = {
            "email": "Email Address",
            "is_vendor": "Register as Vendor",
        }

        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email address",
                "class": "form-control"
            }),

            "is_vendor": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Create a strong password",
            "class": "form-control"
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm your password",
            "class": "form-control"
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control"
        })

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email address",
            "class": "form-control",
            "autocomplete": "email",
        }),
        label="Email Address"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "form-control",
            "autocomplete": "current-password",
        }),
        label="Password"
    )

