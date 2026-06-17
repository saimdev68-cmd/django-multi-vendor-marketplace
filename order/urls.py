from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    # Global customer transaction ledgers
    path("", views.OrderListView.as_view(), name="order_list"),
    path("confirm/", views.OrderConfirmView.as_view(), name="order_confirm"),
    path("delivery/", views.OrderDeliveryView.as_view(), name="order_delivery"),
    
    # Secure Embedded Stripe Funnel Pipelines
    path("checkout/", views.OrderCheckoutView.as_view(), name="order_checkout"),
    path("process-payment/", views.ProcessPaymentOrderCreationView.as_view(), name="process_payment"),
    path("success/", views.LastOrderView.as_view(), name="last_order"),
    
    # Isolated Merchant Realm Management
    path("vendor/", views.VendorOrderListView.as_view(), name="vendor_order_list"),
    path("vendor/<int:pk>/", views.VendorOrderDetailView.as_view(), name="vendor_order_detail"),
]