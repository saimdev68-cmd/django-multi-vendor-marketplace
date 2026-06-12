from django.db import models
from vendor.models import Vendor

# Create your models here.

class Wallet(models.Model):
    vendor = models.OneToOneField(Vendor,on_delete=models.CASCADE,related_name="wallet")
    pending_amount = models.DecimalField(max_digits=12,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor.store_name
    

class Transactions(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,related_name="transactions")
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor.store_name
