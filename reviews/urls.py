from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("write/<int:item_id>/", views.CreateReviewView.as_view(), name="write_review"),
]