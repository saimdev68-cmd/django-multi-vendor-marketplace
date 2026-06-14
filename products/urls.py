from django.urls import path
from . import views

# Global application namespace separation hook
app_name = "products"

urlpatterns = [
    # 1. Base Collection Endpoint
    path("", views.ProductListView.as_view(), name="list"),
    
    # 2. Static Mutation Gates (Placed safely above dynamic parameters)
    path("create/", views.ProductCreateView.as_view(), name="create"),
    
    # 3. Dynamic Member Endpoints (Isolated with trailing resource verbs)
    path("<int:pk>/", views.ProductDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.ProductUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="delete"),
]