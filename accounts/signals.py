from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from buyer.models import Buyer

@receiver(post_save,sender=User)
def create_buyer_signal(sender,instance,created,**kwargs):
    if created:
        Buyer.objects.create(user=instance)
    