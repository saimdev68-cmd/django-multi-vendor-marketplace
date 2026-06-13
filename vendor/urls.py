from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    path("setup/",views.VendorSetupView.as_view(),name="setup"),
    path("detail/",views.VendorDetailView.as_view(),name="detail"),
    path("update/",views.VendorUpdateView.as_view(),name="update"),
    path("dashboard/",views.VendorDashboardView.as_view(),name="vendor_dashboard")
]
