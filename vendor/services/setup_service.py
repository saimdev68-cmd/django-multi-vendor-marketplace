from django.db import transaction
from vendor.forms import VendorForm
from bank_account.forms import BankAccountForm
from .vendor_service import VendorService

class VendorSetupService:

    @staticmethod
    def create_vendor_with_bank(user, post_data, file_data):
        vendor_form = VendorForm(post_data,file_data)
        bank_form = BankAccountForm(post_data)

        if not (vendor_form.is_valid() and bank_form.is_valid()):
            return False, vendor_form, bank_form

        with transaction.atomic():

            vendor = VendorService.create_vendor(
                user=user,
                **vendor_form.cleaned_data
            )

            bank = bank_form.save(commit=False)
            bank.vendor = vendor
            bank.save()

        return vendor, vendor_form, bank_form