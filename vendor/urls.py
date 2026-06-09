from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    path("", views.VendorDetailView.as_view(), name="vendor_detail"),
    path("dashboard/",views.VendorDashboardView.as_view(),name="vendor_dashboard"),
    path("create/",views.VendorCreateView.as_view(),name="vendor_create"),
    path("edit/", views.VendorUpdateView.as_view(), name="vendor_update"),
    path("bank/",views.BankAccountListView.as_view(),name="bank_list"),
    path("bank/detail/<int:pk>/", views.BankAccountDetailView.as_view(), name="bank_detail"),
    path("bank/edit/<int:pk>", views.BankAccountUpdateView.as_view(), name="bank_update"),
]