from django.db import models
from vendor.models import Vendor
from django.core.validators import RegexValidator

# Create your models here.

class BankAccount(models.Model):

    class AccountType(models.TextChoices):
        SAVINGS = "savings", "Savings"
        CURRENT = "current", "Current"

    alphanumeric_validator = RegexValidator(
        regex=r'^[A-Z0-9]{5,50}$',
        message="Must contain only uppercase letters and digits, between 5 and 50 characters."
    )

    vendor = models.OneToOneField(Vendor,on_delete=models.CASCADE,related_name="bank_account")
    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50,validators=[alphanumeric_validator])
    iban_number = models.CharField(max_length=50,unique=True,validators=[alphanumeric_validator])
    account_type = models.CharField(max_length=20,choices=AccountType.choices,default=AccountType.CURRENT)
    is_verified = models.BooleanField(default=False,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"

    def __str__(self):
        return f"{self.bank_name} - {self.account_holder_name}"