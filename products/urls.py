from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    VendorProductListView,
)

app_name = "products"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    path("", VendorProductListView.as_view(), name="vendor_product_list"),
    path("add/", ProductCreateView.as_view(), name="product_create"),
    path("vendor/products/<slug:slug>/edit/", ProductUpdateView.as_view(), name="product-update"),
    path("vendor/products/<slug:slug>/delete/", ProductDeleteView.as_view(), name="product-delete"),
]