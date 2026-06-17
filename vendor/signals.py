from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Vendor, VendorStatusLog, BankAccount, BankAccountStatusLog
from .middleware import get_current_user

# --- AUTOMATIC VENDOR LOGGING ---

@receiver(pre_save, sender=Vendor)
def track_vendor_status_before_save(sender, instance, **kwargs):
    """
    Intercepts the vendor right before saving to check if the status changed.
    Stores the previous status on the instance temporarily in memory.
    """
    if instance.pk:
        try:
            previous_instance = Vendor.objects.get(pk=instance.pk)
            instance._previous_status = previous_instance.status
        except Vendor.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None # New registration

# Update your post_save receivers to match this clean pattern:

@receiver(post_save, sender=Vendor)
def log_vendor_status_after_save(sender, instance, created, **kwargs):
    old_status = getattr(instance, '_previous_status', None)
    new_status = instance.status

    if created or old_status != new_status:
        # Automatically pull the request operator user out of the active running thread!
        current_user = get_current_user()
        # Fallback to None if the mutation happens inside a custom shell script or management command
        operator = current_user if current_user and current_user.is_authenticated else None

        VendorStatusLog.objects.create(
            vendor=instance,
            old_status=old_status,
            new_status=new_status,
            reason=getattr(instance, 'status_notes', ''),
            changed_by=operator
        )


# --- AUTOMATIC BANK ACCOUNT LOGGING ---

@receiver(pre_save, sender=BankAccount)
def track_bank_status_before_save(sender, instance, **kwargs):
    """Caches the old bank account status right before hitting the database."""
    if instance.pk:
        try:
            previous_instance = BankAccount.objects.get(pk=instance.pk)
            instance._previous_status = previous_instance.status
        except BankAccount.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None

@receiver(post_save, sender=BankAccount)
def log_bank_status_after_save(sender, instance, created, **kwargs):
    old_status = getattr(instance, '_previous_status', None)
    new_status = instance.status

    if created or old_status != new_status:
        current_user = get_current_user()
        operator = current_user if current_user and current_user.is_authenticated else None

        BankAccountStatusLog.objects.create(
            bank_account=instance,
            old_status=old_status,
            new_status=new_status,
            reason=getattr(instance, 'status_notes', ''),
            changed_by=operator
        )