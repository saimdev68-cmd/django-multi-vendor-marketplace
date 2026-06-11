from django.urls import path
from . import views

app_name = "bank_account"

urlpatterns = [
    path("",views.BankAccountListView.as_view(),name="bank_account_list"),
    path("create/",views.BankAccountCreateView.as_view(),name="bank_account_create"),
    path("<int:pk>/",views.BankAccountDetailView.as_view(),name="bank_account_detail"),
    path("update/<int:pk>/",views.BankAccountUpdateView.as_view(),name="bank_account_update"),
    path("delete/<int:pk>/",views.BankAccountDeleteView.as_view(),name="bank_account_delete"),
]
