from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.crypto import get_random_string

from cart.models import Cart
from .models import Order, OrderItem


class CheckoutView(LoginRequiredMixin, View):

    def post(self, request):
        buyer = request.user.buyer_profile
        cart = Cart.objects.get(buyer=buyer)

        if not cart.items.exists():
            return redirect("cart-detail")

        # Create Order
        order = Order.objects.create(
            buyer=buyer,
            order_number=get_random_string(10).upper(),
            shipping_address=buyer.address or "No address provided",
            total_amount=cart.total_price()
        )

        # Create Order Items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                vendor=item.product.vendor,
                price=item.product.final_price(),
                quantity=item.quantity
            )

        # Clear cart after order
        cart.items.all().delete()

        return redirect("order-detail", pk=order.id)
    

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class BuyerOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "order/buyer_order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user.buyer_profile)
    

from django.views.generic import DetailView


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "order/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user.buyer_profile)
    
class VendorOrderListView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = "order/vendor_order_list.html"
    context_object_name = "order_items"

    def get_queryset(self):
        return OrderItem.objects.filter(
            vendor=self.request.user.vendor_profile
        )