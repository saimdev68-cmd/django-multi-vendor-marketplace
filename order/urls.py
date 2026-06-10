from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("confirm/",views.ConfirmView.as_view(),name="confirm"),
    path("delivery/",views.DeliveryView.as_view(),name="delivery"),
    path("payment/",views.PaymentView.as_view(),name="payment"),
    path("last_order/",views.LastOrderView.as_view(),name="last_order")
]
