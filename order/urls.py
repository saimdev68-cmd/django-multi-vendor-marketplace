from django.urls import path
from .views import (
    CheckoutView,
    BuyerOrderListView,
    OrderDetailView,
    VendorOrderListView,
)

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path("orders/", BuyerOrderListView.as_view(), name="buyer-orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),

    path("vendor/orders/", VendorOrderListView.as_view(), name="vendor-orders"),
]