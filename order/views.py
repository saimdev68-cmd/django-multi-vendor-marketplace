from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView , FormView , ListView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart
from .forms import DeliveryForm
from .models import Order , OrderItem
from django.shortcuts import redirect

class OrderConfirmView(LoginRequiredMixin,TemplateView):
    template_name = "order_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(buyer=self.request.user.buyer)
        items = cart.items.all()
        context["items"] = items
        return context
    
class OrderDeliveryView(LoginRequiredMixin,FormView):
    template_name = "order_delivery.html"
    form_class = DeliveryForm
    success_url = reverse_lazy("order:order_checkout")

    def form_valid(self, form):
        name = form.cleaned_data.get("name")
        phone = form.cleaned_data.get("phone")
        address = form.cleaned_data.get("address")
        self.request.session["name"] = name
        self.request.session["phone"] = phone
        self.request.session["address"] = address
        return super().form_valid(form)
    
class OrderCheckoutView(LoginRequiredMixin,View):
    def post(self,request):
        name = request.session.get("name")
        phone = request.session.get("phone")
        address = request.session.get("address")
        cart = Cart.objects.get(buyer=request.user.buyer)
        items = cart.items.all()
        order = Order.objects.create(buyer=request.user.buyer,name=name,phone_number=phone,shipping_address=address)
        total = 0
        for item in items:
            order_item = OrderItem.objects.create(
                product = item.product,
                order = order,
                vendor = item.product.vendor,
                price = item.product.price,
                quantity = item.quantity
            )
            total += order_item.total_price
        order.total_amount = total
        order.save()
        return redirect ("order:last_order")
    
class LastOrderView(LoginRequiredMixin,TemplateView):
    template_name = "last_order.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = Order.objects.filter(buyer=self.request.user.buyer).last()
        return context
    
class OrderListView(LoginRequiredMixin,ListView):
    template_name = "order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user.buyer)
    
class VendorOrderListView(LoginRequiredMixin,ListView):
    template_name = "vendor_order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return OrderItem.objects.filter(vendor=self.request.user.vendor)     

class VendorOrderDetailView(LoginRequiredMixin,DetailView):
    template_name = "vendor_order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return OrderItem.objects.filter(vendor=self.request.user.vendor)   