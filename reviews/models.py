from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from buyer.models import Buyer
from order.models import OrderItem  #


class Review(models.Model):
    """
    Stores product reviews tied directly to verified OrderItem transaction records.
    Provides a seamless database lookup chain: Review -> OrderItem -> Product.
    """
    buyer = models.ForeignKey(
        Buyer, 
        on_delete=models.CASCADE, 
        related_name="reviews"
    )
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="review",
        help_text="The specific purchased line item this review belongs to."
    )
    
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, "Rating must be at least 1 star."),
            MaxValueValidator(5, "Rating cannot exceed 5 stars.")
        ]
    )
    comment = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marketly_reviews"
        ordering = ["-created_at"]

    def __str__(self):
        product_name = self.order_item.product.name if self.order_item.product else "Unknown Product"
        return f"{self.buyer.user.email} - {product_name} ({self.rating}★)"

    def clean(self):
        """
        Defensive check: Validates that the buyer submitting the review is 
        the exact same buyer who placed the global transaction order.
        """
        super().clean()
        # Navigate the relational chain: OrderItem -> VendorOrder -> Order -> Buyer
        if self.order_item and self.order_item.vendor_order.order.buyer != self.buyer:
            raise ValidationError("Security violation: You cannot review an item from an order you did not purchase.")