from django.db import models
from django.db.models import F, Sum
from buyer.models import Buyer
from products.models import Product

class Cart(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marketly_carts"
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"Cart of {self.buyer.user.username}"
    
    @property
    def total_price(self) -> float:
        """Optimized aggregation calculation avoiding single instance iteration loop N+1s."""
        # Fallback to zero if cart is empty
        aggregation = self.items.aggregate(
            total=Sum(F("quantity") * F("product__price")) # Adjust 'price' to your actual Product cost field name
        )
        return aggregation["total"] or 0.0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marketly_cart_items"
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="unique_cart_product")
        ]

    def __str__(self) -> str:
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self) -> float:
        return self.product.price * self.quantity

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)