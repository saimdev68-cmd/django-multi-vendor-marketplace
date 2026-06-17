from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Cart
from .services.cart import CartService

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            CartService.add_item(buyer=request.user.buyer, product_id=pk)
        except Exception as e:
            messages.error(request, str(e))
        return redirect("cart:detail")


class CartDetailView(LoginRequiredMixin, DetailView):
    template_name = "cart_detail.html"
    context_object_name = "cart"

    def get_object(self, queryset=None) -> Cart:
        # Uses explicit prefetch_related optimization to bundle entire cart payload into 2 clean SQL queries
        return Cart.objects.select_related("buyer__user").prefetch_related("items__product").get(
            buyer=self.request.user.buyer
        )


class RemoveFromCart(LoginRequiredMixin, View):
    def post(self, request, pk):
        CartService.remove_item(cart_item_id=pk)
        return redirect("cart:detail")


class IncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            CartService.increment_quantity(cart_item_id=pk)
        except Exception as e:
            messages.error(request, str(e))
        return redirect("cart:detail")


class DecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        CartService.decrement_quantity(cart_item_id=pk)
        return redirect("cart:detail")