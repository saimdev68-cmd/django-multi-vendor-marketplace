from django import forms

class DeliveryForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField()
    address = forms.Textarea()
