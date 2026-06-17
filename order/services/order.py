from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from decimal import Decimal
from cart.models import Cart
from ..models import Order, VendorOrder, OrderItem


class OrderService:
    """
    Business service layer orchestrating split-order checkout funnels.
    Handles inventory thread-locking, multi-vendor bundling, and cart disposal.
    """

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(buyer, checkout_data: dict) -> Order:
        """
        Transforms an active buyer Cart into a structured Split-Order tree.
        Locks product stock rows inline to securely guarantee inventory counts.
        """
        # Fetch the customer's cart along with relational item data
        cart = get_object_or_404(
            Cart.objects.prefetch_related("items__product__vendor"), 
            buyer=buyer
        )
        cart_items = cart.items.all()

        if not cart_items.exists():
            raise ValidationError("Your shopping cart is completely empty. Transaction aborted.")

        # 1. Instantiate Global Financial Container Parent Record
        order = Order(
            buyer=buyer,
            name=checkout_data["name"],
            phone_number=checkout_data["phone_number"],
            country=checkout_data["country"],
            city=checkout_data["city"],
            shipping_address=checkout_data["shipping_address"],
            total_amount=Decimal("0.00")  # Calculated incrementally below
        )
        order.full_clean()
        order.save()

        global_total = Decimal("0.00")
        vendor_buckets = {}

        # 2. Iterate line items and dynamically evaluate vendor groupings
        for item in cart_items:
            product = item.product
            
            # Pessimistic database locking prevents multi-user concurrency overselling conditions
            product_locked = (
                product.__class__.objects.select_for_update()
                .get(pk=product.pk)
            )

            if product_locked.stock < item.quantity:
                raise ValidationError(
                    f"Stock allocation failure for '{product_locked.name}'. "
                    f"Only {product_locked.stock} available, but you requested {item.quantity}."
                )

            # Deduct inventory quantities safely
            product_locked.stock -= item.quantity
            product_locked.save(update_fields=["stock", "updated_at"])

            vendor = product_locked.vendor
            if vendor.id not in vendor_buckets:
                # Instantiate an isolated Vendor fulfillment bundle package
                vendor_order = VendorOrder(
                    order=order,
                    vendor=vendor,
                    vendor_subtotal=Decimal("0.00")
                )
                vendor_order.full_clean()
                vendor_order.save()
                
                vendor_buckets[vendor.id] = {
                    "instance": vendor_order,
                    "subtotal": Decimal("0.00"),
                    "items_to_create": []
                }

            # Capture accurate item financial variables at the exact millisecond of checkout
            item_price = Decimal(str(product_locked.price))
            item_subtotal = item_price * item.quantity
            
            vendor_buckets[vendor.id]["subtotal"] += item_subtotal
            global_total += item_subtotal

            # Queue historical OrderItem lines for compilation
            order_item = OrderItem(
                vendor_order=vendor_buckets[vendor.id]["instance"],
                product=product_locked,
                price=item_price,
                quantity=item.quantity
            )
            vendor_buckets[vendor.id]["items_to_create"].append(order_item)

        # 3. Batch commit line updates using bulk operations
        for bucket_id, bucket in vendor_buckets.items():
            vendor_order_instance = bucket["instance"]
            vendor_order_instance.vendor_subtotal = bucket["subtotal"]
            vendor_order_instance.save(update_fields=["vendor_subtotal", "updated_at"])

            # Bulk save individual lines efficiently in a single query block
            OrderItem.objects.bulk_create(bucket["items_to_create"])

        # Commit final financial balance updates onto the master bill invoice container
        order.total_amount = global_total
        order.save(update_fields=["total_amount", "updated_at"])

        # 4. Wipe active cart item contents now that persistence transitions are completed
        cart_items.delete()

        return order