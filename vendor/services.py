from django.db import transaction
from .forms import VendorForm
from bank_account.forms import BankAccountForm

class VendorSetupService:

    @staticmethod
    @transaction.atomic
    def create_vendor_with_bank(user, vendor_form_data, vendor_file_data, bank_account_form_data):

        vendor_form = VendorForm(vendor_form_data, vendor_file_data)
        bank_account_form = BankAccountForm(bank_account_form_data)

        if not (vendor_form.is_valid() and bank_account_form.is_valid()):
            return False, vendor_form, bank_account_form

        vendor = vendor_form.save(commit=False)
        vendor.owner = user
        vendor.save()

        bank_account = bank_account_form.save(commit=False)
        bank_account.vendor = vendor
        bank_account.save()

        return vendor, vendor_form, bank_account_form
