from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    # Main resource view mapping
    path("", views.CartDetailView.as_view(), name="detail"),
    
    # Action endpoints - explicit parameters passing clean resource IDs
    path(
        "add/<int:pk>/", 
        views.AddToCartView.as_view(), 
        name="add_to_cart"
    ),
    path(
        "item/<int:pk>/remove/", 
        views.RemoveFromCart.as_view(), 
        name="remove_from_cart"
    ),
    path(
        "item/<int:pk>/increase/", 
        views.IncreaseQuantityView.as_view(), # Checked: Points to corrected Q-syntax view class
        name="increase_quantity"
    ),
    path(
        "item/<int:pk>/decrease/", 
        views.DecreaseQuantityView.as_view(), # Checked: Points to corrected Q-syntax view class
        name="decrease_quantity"
    ),
]