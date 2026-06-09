from django.db import models
from buyer.models import Buyer


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_number = models.CharField(max_length=20, unique=True)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    shipping_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number
    
from django.db import models
from product.models import Product
from vendor.models import Vendor


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.price * self.quantity