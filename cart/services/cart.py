from django.db import transaction
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from products.models import Product
from ..models import Cart, CartItem

class CartService:
    """
    Dedicated enterprise service layer orchestrating atomic cart workflows.
    Encapsulates all calculations, validations, and state changes.
    """
    
    @staticmethod
    @transaction.atomic
    def add_item(buyer, product_id: int) -> CartItem:
        # select_for_update prevents concurrent race conditions on product stock checks
        product = get_object_or_404(Product.objects.select_for_update(), pk=product_id)
        cart, _ = Cart.objects.get_or_create(buyer=buyer)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            if cart_item.quantity >= product.stock:
                raise ValidationError(f"Cannot add more items. Only {product.stock} units available.")
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity", "updated_at"])
        else:
            if product.stock < 1:
                cart_item.delete()
                raise ValidationError("This product is currently out of stock.")
                
        return cart_item

    @staticmethod
    @transaction.atomic
    def remove_item(cart_item_id: int) -> None:
        cart_item = get_object_or_404(CartItem, pk=cart_item_id)
        cart_item.delete()

    @staticmethod
    @transaction.atomic
    def increment_quantity(cart_item_id: int) -> CartItem:
        cart_item = get_object_or_404(
            CartItem.objects.select_related("product").select_for_update(of=("product",)), 
            pk=cart_item_id
        )
        if cart_item.quantity >= cart_item.product.stock:
            raise ValidationError(f"Maximum allocation reached. Only {cart_item.product.stock} units available.")
        
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity", "updated_at"])
        return cart_item

    @staticmethod
    @transaction.atomic
    def decrement_quantity(cart_item_id: int) -> CartItem | None:
        cart_item = get_object_or_404(CartItem.objects.select_related("product"), pk=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save(update_fields=["quantity", "updated_at"])
            return cart_item
        
        cart_item.delete()
        return None