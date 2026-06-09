from django.urls import path
from .views import (
    add_to_cart,
    CartDetailView,
    remove_from_cart,
    update_cart,
)

app_name = "cart"

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart_detail"),

    path("cart/add/<int:pk>", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:item_id>/", update_cart, name="update_cart"),
]