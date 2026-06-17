from django.db import models
from decimal import Decimal
from vendor.models import Vendor
# If your order app models are in the same project, you can import Order or VendorOrder to link them
# from order.models import Order


class Wallet(models.Model):
    """
    Tracks real-time merchant balances. Separate ledgers prevent cash leakage
    by ensuring escrow amounts remain locked until safe fulfillment delivery windows close.
    """
    vendor = models.OneToOneField(
        Vendor, 
        on_delete=models.CASCADE, 
        related_name="wallet"
    )
    available_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00"),
        help_text="Cleared funds ready for vendor payout withdrawal request."
    )
    pending_balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00"),
        help_text="Funds locked in escrow from recent orders awaiting delivery confirmation."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marketly_wallets"
        verbose_name = "Vendor Wallet"
        verbose_name_plural = "Vendor Wallets"

    def __str__(self):
        return f"{self.vendor.store_name} Balance: Slot [Avail: ${self.available_balance} | Pend: ${self.pending_balance}]"


class Transaction(models.Model):
    """
    An immutable financial ledger recording every incoming credit (earnings) 
    and outgoing debit (withdrawals, refunds) for accounting audit safety.
    """
    class TransactionType(models.TextChoices):
        CREDIT = "credit", "Credit (Incoming Revenue)"
        DEBIT = "debit", "Debit (Payout Withdrawal)"
        REFUND = "refund", "Refund (Customer Chargeback)"

    class TransactionStatus(models.TextChoices):
        PENDING = "pending", "Pending Escrow"
        COMPLETED = "completed", "Settled & Cleared"
        FAILED = "failed", "Failed/Cancelled"

    wallet = models.ForeignKey(
        Wallet, 
        on_delete=models.CASCADE, 
        related_name="ledger_transactions"
    )
    # Keeping a direct lookup to Vendor for shortcut filtering in merchant dashboards
    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.CASCADE, 
        related_name="financial_transactions"
    )
    
    # Financial data constraints
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(
        max_length=20, 
        choices=TransactionType.choices, 
        default=TransactionType.CREDIT
    )
    status = models.CharField(
        max_length=20, 
        choices=TransactionStatus.choices, 
        default=TransactionStatus.PENDING
    )
    
    # Audit trail details
    reference_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="External processor hash, payout request batch key, or system tracker token."
    )
    description = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Human-readable summary of the movement (e.g. 'Payout payout_ref_9921', 'Order revenue #104')."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "marketly_transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["vendor", "transaction_type"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        type_arrow = "↗" if self.transaction_type == self.TransactionType.CREDIT else "↘"
        return f"[{self.get_status_display()}] {self.vendor.store_name} {type_arrow} ${self.amount}"