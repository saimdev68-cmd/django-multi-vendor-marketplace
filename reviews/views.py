from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from order.models import OrderItem
from .forms import ProductReviewForm
from .models import Review


class CreateReviewView(LoginRequiredMixin, CreateView):
    """
    Handles the presentation and submission of a product review form.
    Ties the review directly to an OrderItem line record.
    """
    model = Review
    form_class = ProductReviewForm
    template_name = "reviews/submit_review.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Defensive perimeter guard: Ensures the order item exists, belongs to 
        the logged-in buyer, and hasn't been reviewed already.
        """
        self.order_item = get_object_or_404(OrderItem, id=self.kwargs.get("item_id"))
        
        # Security Check: Does this order item belong to the current buyer?
        if self.order_item.vendor_order.order.buyer != request.user.buyer:
            raise PermissionDenied("You do not have permission to review this item.")
        
        # Integrity Check: Has this item already been reviewed?
        if hasattr(self.order_item, "review"):
            messages.warning(request, "You have already submitted a review for this item.")
            return redirect("order:order_list")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Injects the order item details into the template block context."""
        context = super().get_context_data(**kwargs)
        context["item"] = self.order_item
        return context

    def form_valid(self, form):
        """Atomically maps the user identity and order item to the model instance."""
        review = form.save(commit=False)
        review.buyer = self.request.user.buyer
        review.order_item = self.order_item
        review.save()
        
        messages.success(self.request, "Thank you! Your verified review has been published.")
        return redirect("order:order_list")