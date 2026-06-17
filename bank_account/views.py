from vendor.models import BankAccount
from django.views.generic import DetailView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from vendor.forms import BankAccountForm
from django.urls import reverse_lazy

# Create your views here.
    
class BankDetailView(LoginRequiredMixin,DetailView):
    template_name = "bank_detail.html"
    context_object_name = "bank"

    def get_object(self, queryset = None):
        return BankAccount.objects.select_related('vendor').get(vendor=self.request.user.vendor)
    
class BankUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "bank_update.html"
    form_class = BankAccountForm
    success_url = reverse_lazy("bank:detail")

    def get_object(self, queryset = None):
        return BankAccount.objects.get(vendor=self.request.user.vendor)
