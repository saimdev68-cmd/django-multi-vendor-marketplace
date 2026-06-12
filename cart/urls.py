from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("",views.CartDetailView.as_view(),name="cart_detail"),
    path("add_to_cart/<int:pk>/",views.AddToCartView.as_view(),name="add_to_cart"),
    path("remove_from_cart/<int:pk>/",views.RemoveFromCart.as_view(),name="remove_from_cart"),
    path("increase_quantity/<int:pk>/",views.IncreaseOuantityView.as_view(),name="increase_quantity"),
    path("decrease_quantity/<int:pk>/",views.DecreaseOuantityView.as_view(),name="decrease_quantity"),
]
