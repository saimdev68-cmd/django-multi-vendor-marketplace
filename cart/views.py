from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from buyer.models import Buyer 
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    buyer = request.user.buyer
    cart , create = Cart.objects.get_or_create(buyer=buyer)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        item.quantity += 1
        item.save()
    return redirect("cart:cart_detail")


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart_detail.html"
    context_object_name = "cart"

    def get_object(self):
        cart, created = Cart.objects.get_or_create(
            buyer=self.request.user.buyer
        )
        return cart

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart:cart_detail")


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    action = request.GET.get("action")

    if action == "increase":
        item.quantity += 1
    elif action == "decrease" and item.quantity > 1:
        item.quantity -= 1

    item.save()
    return redirect("cart:cart_detail")