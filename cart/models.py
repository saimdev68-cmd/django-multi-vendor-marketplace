from django.db import models
from buyer.models import Buyer
from products.models import Product


class Cart(models.Model):

    buyer = models.OneToOneField(
        Buyer,
        on_delete=models.CASCADE,
        related_name="cart"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.buyer.user.username}"

    def total_price(self):
        items = self.items.all()
        return sum(item.total_price() for item in items)
    
class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")  # prevent duplicate product rows

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def total_price(self):
        price = self.product.final_price()
        return price * self.quantity