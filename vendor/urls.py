from django.urls import path
from . import views

app_name = "vendor"

urlpatterns = [
    path("setup/",views.VendorSetupView.as_view(),name="setup"),
    path("detail/",views.VendorDetailView.as_view(),name="detail"),
    path("update/",views.VendorUpdateView.as_view(),name="update"),
    path("dashboard/",views.VendorDashboardView.as_view(),name="dashboard"),
    path("ajax/load-cities/", views.load_cities_ajax, name="ajax_load_cities"),
]
