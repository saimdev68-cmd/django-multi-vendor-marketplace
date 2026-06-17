from django.db import models
from buyer.models import Buyer
from products.models import Product
from vendor.models import Vendor , Country , City

class Order(models.Model):
    """
    Financial & Customer Container. 
    Tracks the global checkout session and absolute transaction totals.
    """
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, related_name="orders")
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Global customer delivery context
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,null=True)
    shipping_address = models.TextField()
    
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "marketly_orders"


class VendorOrder(models.Model):
    """
    The Logistics & Fulfillment Engine.
    Isolates each vendor's individual package life cycle completely.
    """
    class FulfillmentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        RETURN_REQUESTED = "return_requested", "Return Requested"
        RETURNED = "returned", "Returned"
        CANCELLED = "cancelled", "Cancelled"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="vendor_orders")
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="vendor_fulfillments")
    
    status = models.CharField(max_length=25, choices=FulfillmentStatus.choices, default=FulfillmentStatus.PENDING)
    vendor_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Isolated tracking mechanics per vendor
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    carrier_name = models.CharField(max_length=50, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "marketly_vendor_orders"
        indexes = [
            models.Index(fields=["vendor", "status"]),
        ]


class OrderItem(models.Model):
    """
    Individual purchase line records linked directly to their respective logistics package.
    """
    # Pointing to the VendorOrder breaks dependency on global order statuses
    vendor_order = models.ForeignKey(VendorOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "marketly_order_items"
        
    @property
    def total_price(self) -> float:
        return self.price * self.quantity