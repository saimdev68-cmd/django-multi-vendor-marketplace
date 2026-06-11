from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("category/",views.CategoryListView.as_view(),name="category_list"),
    path("product/",views.ProductListView.as_view(),name="product"),
    path("vendor/list/",views.VendorListView.as_view(),name="vendor_list"),
]
