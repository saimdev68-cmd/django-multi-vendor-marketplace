from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    path("create/",views.VendorCreateView.as_view(),name="vendor_create"),
    path("detail/",views.VendorDetailView.as_view(),name="vendor_detail"),
    path("update/",views.VendorUpdateView.as_view(),name="vendor_update"),
    path("dashboard/",views.VendorDashboardView.as_view(),name="vendor_dashboard")
]
