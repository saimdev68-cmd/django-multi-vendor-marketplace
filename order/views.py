import uuid
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, FormView
from .models import OrderItem, Order 
from cart.models import Cart
from .forms import DeliveryForm, PaymentForm

class ConfirmView(LoginRequiredMixin, DetailView):
    template_name = "confirm.html"
    context_object_name = "cart"

    def get_object(self, queryset=None):
        return Cart.objects.get(buyer=self.request.user.buyer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_step'] = 1
        return context

class DeliveryView(LoginRequiredMixin, FormView):
    template_name = "delivery.html"
    form_class = DeliveryForm
    success_url = reverse_lazy("order:payment")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_step'] = 2
        return context

    def form_valid(self, form):
        # Fixed typo from cleaned_date to cleaned_data
        name = form.cleaned_data.get("name")
        address = form.cleaned_data.get("address")
        phone_number = form.cleaned_data.get("phone_number")
        
        self.request.session["name"] = name
        self.request.session["address"] = address
        self.request.session["phone_number"] = phone_number
        return super().form_valid(form)
    
class PaymentView(LoginRequiredMixin, FormView):
    template_name = "payment.html"
    form_class = PaymentForm
    success_url = reverse_lazy("order:last_order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_step'] = 3
        return context

    def form_valid(self, form):
        buyer = self.request.user.buyer
        try:
            cart = Cart.objects.get(buyer=buyer)
        except Cart.DoesNotExist:
            return redirect("cart:view_cart") # Redirect back if cart became empty

        # Grab cached values from session store
        session_address = self.request.session.get("address", "No address provided")
        session_name = self.request.session.get("name", "")
        session_phone = self.request.session.get("phone_number", "")
        full_shipping_payload = f"{session_name}\n{session_address}\nTel: {session_phone}"

        # 1. Create Order instance
        order = Order.objects.create(
            buyer=buyer,
            order_number=f"ORD-{uuid.uuid4().hex[:12].upper()}",
            status=Order.OrderStatus.CONFIRMED,
            payment_status=Order.PaymentStatus.PAID,
            total_amount=cart.total_price(), # Assuming total_price is a method or property
            shipping_address=full_shipping_payload
        )

        # 2. Extract Cart items into persistent OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                vendor=item.product.vendor, # Mapping relational vendor data 
                price=item.product.price,
                quantity=item.quantity
            )

        # 3. Clear temporary cart state
        cart.items.all().delete() 
        
        # Flush sensitive session addresses securely
        self.request.session.pop("name", None)
        self.request.session.pop("address", None)
        self.request.session.pop("phone_number", None)

        return super().form_valid(form)

class LastOrderView(LoginRequiredMixin, DetailView):
    template_name = "last_order.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return Order.objects.filter(buyer=self.request.user.buyer).order_by('-created_at').first()