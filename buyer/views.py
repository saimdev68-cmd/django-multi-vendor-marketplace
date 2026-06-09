from django.views.generic import DetailView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Buyer
from .form import BuyerForm
from django.urls import reverse_lazy


class BuyerDetailView(LoginRequiredMixin, DetailView):
    model = Buyer
    template_name = "buyer_detail.html"
    context_object_name = "buyer"

    def get_object(self):
        return self.request.user.buyer 
    
class BuyerUpdateView(LoginRequiredMixin, UpdateView):
    model = Buyer
    form_class = BuyerForm
    template_name = "buyer_update.html"
    success_url = reverse_lazy("buyer:buyer_detail")

    def get_object(self):
        return self.request.user.buyer