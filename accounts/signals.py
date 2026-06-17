from django.db.models.signals import post_save
from .models import User
from buyer.models import Buyer
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_buyer_profile(sender,instance,created,**kwargs):
    if created:
        Buyer.objects.create(user=instance)