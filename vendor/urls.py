from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    path("create/",views.VendorCreateView.as_view(),name="vendor_create")
]
