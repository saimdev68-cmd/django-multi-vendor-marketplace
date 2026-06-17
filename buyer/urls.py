from django.urls import path
from . import views

app_name = "buyer"

urlpatterns = [
    path("", views.BuyerDetailView.as_view(), name="detail"),
    path("edit/", views.BuyerUpdateView.as_view(), name="update"),
]