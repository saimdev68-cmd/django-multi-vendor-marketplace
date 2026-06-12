from django.contrib import admin
from .models import Wallet , Transactions

# Register your models here.

class TransactionInline(admin.TabularInline):
    model = Transactions
    extra = 0

@admin.register(Wallet)
class WalletAdminn(admin.ModelAdmin):
    inlines = [TransactionInline]