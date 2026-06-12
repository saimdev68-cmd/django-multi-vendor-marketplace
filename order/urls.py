from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("",views.OrderListView.as_view(),name="order_list"),
    path("vendor/",views.OrderListView.as_view(),name="vendor_order_list"),
    path("confirm/",views.OrderConfirmView.as_view(),name="order_confirm"),
    path("delivery/",views.OrderDeliveryView.as_view(),name="order_delivery"),
    path("checkout/",views.OrderCheckoutView.as_view(),name="order_checkout"),
    path("vendor/<int:pk>/",views.VendorOrderDetailView.as_view(),name="vendor_order_detail")
]
