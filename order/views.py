import os
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView

from cart.models import Cart
from vendor.models import Country, City
from .forms import OrderCheckoutForm
from .models import Order, VendorOrder, OrderItem
from .services.order import OrderService

# Initialize Stripe Client Engine Driver
stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", os.getenv("STRIPE_SECRET_KEY"))


class OrderConfirmView(LoginRequiredMixin, TemplateView):
    """
    Step 1: Displays an in-memory cart breakdown summary review page before checkout forms.
    """
    template_name = "order_confirm.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(
            Cart.objects.prefetch_related("items__product"), 
            buyer=self.request.user.buyer
        )
        context["items"] = cart.items.all()
        context["cart"] = cart
        return context


class OrderDeliveryView(LoginRequiredMixin, FormView):
    """
    Step 2: Collects granular shipping targets and saves input references inside request sessions.
    """
    template_name = "order_delivery.html"
    form_class = OrderCheckoutForm
    success_url = reverse_lazy("order:order_checkout")

    def form_valid(self, form):
        """Caches validated form details securely inside session cookies."""
        cleaned = form.cleaned_data
        self.request.session["checkout_name"] = cleaned.get("name")
        self.request.session["checkout_phone"] = cleaned.get("phone_number")
        self.request.session["checkout_country_id"] = cleaned.get("country").id
        self.request.session["checkout_city_id"] = cleaned.get("city").id
        self.request.session["checkout_address"] = cleaned.get("shipping_address")
        return super().form_valid(form)


class OrderCheckoutView(LoginRequiredMixin, TemplateView):
    """
    Step 3: Embedded Stripe Payment Panel.
    Initializes a PaymentIntent and passes its Client Secret to local Stripe Elements JS modules.
    """
    template_name = "order_checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buyer = self.request.user.buyer

        # Enforce sequence: Guarantee shipping sessions haven't cleared or expired
        if "checkout_name" not in self.request.session:
            raise ValidationError("Checkout context expired. Please re-enter your delivery location details.")

        cart = get_object_or_404(Cart, buyer=buyer)
        total_amount_cents = int(cart.total_price * 100)  # Stripe API computes using the lowest currency fraction

        try:
            # Instantiate a Stripe transaction ledger token intent
            intent = stripe.PaymentIntent.create(
                amount=total_amount_cents,
                currency="usd",
                automatic_payment_methods={"enabled": True},
                metadata={
                    "buyer_id": buyer.id,
                    "buyer_email": self.request.user.email
                }
            )
            context["client_secret"] = intent.client_secret
            context["stripe_publishable_key"] = getattr(settings, "STRIPE_PUBLISHABLE_KEY", os.getenv("STRIPE_PUBLISHABLE_KEY"))
            context["total_amount"] = cart.total_price
        except stripe.error.StripeError as e:
            messages.error(self.request, f"Gateway configuration communication error: {str(e)}")
            context["client_secret"] = None

        return context


class ProcessPaymentOrderCreationView(LoginRequiredMixin, View):
    """
    Post-Payment Handler View.
    Triggered via JavaScript POST immediately after Stripe Elements client-side authorization clears.
    """
    def post(self, request, *args, **kwargs):
        session = request.session
        payment_intent_id = request.POST.get("payment_intent_id")

        if not payment_intent_id:
            messages.error(request, "Transactional token identity verification missing from gateway provider.")
            return redirect("cart:detail")

        # Resolve explicit ForeignKey instances corresponding to the cached session identifiers
        country = get_object_or_404(Country, id=session.get("checkout_country_id"))
        city = get_object_or_404(City, id=session.get("checkout_city_id"))

        checkout_data = {
            "name": session.get("checkout_name"),
            "phone_number": session.get("checkout_phone"),
            "country": country,
            "city": city,
            "shipping_address": session.get("checkout_address"),
        }

        try:
            # Generate the split-order database structures atomically via our service layer pipeline
            order = OrderService.create_order_from_cart(buyer=request.user.buyer, checkout_data=checkout_data)
            
            # Lock tracking keys and flag payments as cleared
            order.stripe_payment_intent_id = payment_intent_id
            order.payment_status = Order.PaymentStatus.PAID
            order.save(update_fields=["stripe_payment_intent_id", "payment_status", "updated_at"])
            
            # Erase used transient session memory values safely
            for key in list(session.keys()):
                if key.startswith("checkout_"):
                    del session[key]

            return redirect("order:last_order")

        except Exception as e:
            messages.error(request, f"Order persistence instantiation failed: {str(e)}")
            return redirect("cart:detail")


class LastOrderView(LoginRequiredMixin, TemplateView):
    """
    Step 4: Fulfillment Confirmation View. Displays the buyer's post-checkout breakdown status.
    """
    template_name = "last_order.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optimizes performance by prefetching split-order vendor components
        context["order"] = Order.objects.filter(buyer=self.request.user.buyer).prefetch_related(
            "vendor_orders__items__product"
        ).last()
        return context


class OrderListView(LoginRequiredMixin, ListView):
    """Comprehensive buyer transaction summary interface ledger history."""
    template_name = "order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user.buyer).prefetch_related("vendor_orders")


# =====================================================================
# VENDOR REALM OPERATIONS (ISOLATED SEGMENTS)
# =====================================================================

class VendorOrderListView(LoginRequiredMixin, ListView):
    """Renders isolated vendor dashboard package lists without exposing overall billing contexts."""
    template_name = "vendor_order_list.html"
    context_object_name = "vendor_orders"

    def get_queryset(self):
        # Optimized database scan isolates merchant access strictly to their own fulfillment bundles
        return VendorOrder.objects.filter(
            vendor=self.request.user.vendor
        ).select_related("order__buyer__user").prefetch_related("items__product")


class VendorOrderDetailView(LoginRequiredMixin, DetailView):
    """Enables individual item status adjustments and logistics configurations."""
    template_name = "vendor_order_detail.html"
    context_object_name = "vendor_order"

    def get_queryset(self):
        return VendorOrder.objects.filter(vendor=self.request.user.vendor).prefetch_related("items__product")