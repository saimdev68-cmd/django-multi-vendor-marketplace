from django.shortcuts import get_object_or_404, redirect
from .models import Cart, CartItem
from buyer.models import Buyer 
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views import View


class AddToCartView(LoginRequiredMixin,View):
    def post(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        cart = Cart.objects.get(buyer=request.user.buyer)
        cart_item , created = CartItem.objects.get_or_create(product=product,cart=cart)
        if not created:
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart.save()
            return redirect ("cart:cart_detail")


class CartDetailView(LoginRequiredMixin, DetailView):
    template_name = "cart_detail.html"
    context_object_name = "cart"

    def get_object(self, queryset = None):
        return Cart.objects.get(buyer=self.request.user.buyer)

class RemoveFromCart(LoginRequiredMixin,View):
    def post(self,request,pk):
        cart_item = get_object_or_404(CartItem,pk=pk)
        cart_item.delete()
        return redirect ("cart:cart_detail")
    
class IncreaseOuantityView(LoginRequiredMixin,View):
    def post(self,request,pk):
        cart_item = get_object_or_404(CartItem,pk=pk)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        return redirect ("cart:cart_detail")
    
class DecreaseOuantityView(LoginRequiredMixin,View):
    def post(self,request,pk):
        cart_item = get_object_or_404(CartItem,pk=pk)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect ("cart:cart_detail")