from django.views.generic import ListView , CreateView, UpdateView , DetailView , DeleteView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
from django.urls import reverse_lazy



class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(status="active")
    
class VendorProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "vendor_product_list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    
from django.views.generic import DetailView


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(status="active")
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("products:vendor_product_list")

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        return super().form_valid(form)
    

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = reverse_lazy("vendor-product-list")

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor_profile)
    

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product/product_confirm_delete.html"
    success_url = reverse_lazy("vendor-product-list")

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor_profile)