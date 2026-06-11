from django.shortcuts import render , redirect
from .models import BankAccount
from django.views.generic import ListView , CreateView , DeleteView , DetailView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from vendor.models import Vendor
from .forms import BankAccountForm
from django.urls import reverse_lazy

# Create your views here.

class BankAccountListView(LoginRequiredMixin,ListView):
    template_name = "bank_account_list.html"
    context_object_name = "bank_accounts"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        vendor = Vendor.objects.filter(owner=user).exists()
        if user.is_vendor and not vendor:
            return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return BankAccount.objects.filter(vendor=self.request.user.vendor)
    
class BankAccountDetailView(LoginRequiredMixin,DetailView):
    template_name = "bank_account_detail.html"
    context_object_name = "bank_account"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        vendor = Vendor.objects.filter(owner=user).exists()
        if user.is_vendor and not vendor:
            return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return BankAccount.objects.filter(vendor=self.request.user.vendor)
    
class BankAccountCreateView(LoginRequiredMixin,CreateView):
    template_name = "bank_account_form.html"
    form_class = BankAccountForm
    success_url = reverse_lazy("bank_account:bank_account_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        vendor = Vendor.objects.filter(owner=user).exists()
        if user.is_vendor and not vendor:
            return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        return super().form_valid(form)
    
class BankAccountUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "bank_account_form.html"
    form_class = BankAccountForm
    success_url = reverse_lazy("bank_account:bank_account_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        vendor = Vendor.objects.filter(owner=user).exists()
        if user.is_vendor and not vendor:
            return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

class BankAccountDeleteView(LoginRequiredMixin,DeleteView):
    success_url = reverse_lazy("bank_account:bank_account_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        vendor = Vendor.objects.filter(owner=user).exists()
        if user.is_vendor and not vendor:
            return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)