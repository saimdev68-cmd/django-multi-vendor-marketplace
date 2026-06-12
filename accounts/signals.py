from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from buyer.models import Buyer

@receiver(post_save,sender=User)
def create_buyer_signal(sender,instance,created,**kwargs):
    if not instance.is_vendor:
        Buyer.objects.get_or_create(user=instance)