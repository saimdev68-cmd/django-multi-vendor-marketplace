from django.db.models.signals import post_save
from .models import Buyer 
from django.dispatch import receiver
from cart.models import Cart

@receiver(post_save,sender=Buyer)
def create_cart_signal(sender,instance,created,**kwargs):
    if created:
        Cart.objects.get_or_create(buyer=instance)

