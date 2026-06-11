from django.db import models
from vendor.models import Vendor

# Create your models here.

class BankAccount(models.Model):

    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    vendor = models.OneToOneField(Vendor,on_delete=models.CASCADE,related_name="bank_account")
    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    iban_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CURRENT)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.bank_name} - {self.account_holder_name}"