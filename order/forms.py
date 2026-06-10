from django import forms

class DeliveryForm(forms.Form):
    name = forms.CharField()
    phone_number = forms.CharField()
    address = forms.Textarea()


class PaymentForm(forms.Form):
    card_number = forms.CharField()
    card_holder_name = forms.CharField()
    cvv = forms.CharField()
    