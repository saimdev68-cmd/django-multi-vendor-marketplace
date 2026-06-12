from django.shortcuts import render
from django.views.generic import DetailView , ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet , Transactions

# Create your views here.

class WalletDetailView(LoginRequiredMixin,DetailView):
    template_name = "wallet_detail.html"
    context_object_name = "wallet"

    def get_object(self, queryset = None):
        return Wallet.objects.filter(vendor=self.request.user.vendor)

class TransactionListView(LoginRequiredMixin,ListView):
    template_name = "transaction_list.html"
    context_object_name  = "transactions"

    def get_queryset(self):
        return Transactions.objects.filter(vendor=self.request.user.vendor)
    
