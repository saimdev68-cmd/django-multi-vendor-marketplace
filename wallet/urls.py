from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    path("",views.WalletDetailView.as_view(),name="wallet_detail"),
    path("payments/",views.TransactionListView.as_view(),name="transaction_list")
]
