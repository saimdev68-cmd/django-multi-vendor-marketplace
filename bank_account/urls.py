from django.urls import path
from . import views

app_name = "bank"

urlpatterns = [
    path("",views.BankDetailView.as_view(),name="detail"),
    path("update/",views.BankUpdateView.as_view(),name="update"),
]
