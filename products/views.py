from django.shortcuts import render , redirect
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product 
from .forms import ProductForm
from vendor.models import Vendor
from django.urls import reverse_lazy

class ProductListView(LoginRequiredMixin,ListView):
    template_name = "product_list.html"
    context_object_name = "products"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user).exists()
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if vendor and user.vendor.status in [Vendor.VendorStatus.REJECTED,Vendor.VendorStatus.PENDING]:
                return redirect ("vendor:vendor_detail")
            if not vendor:
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    
class ProductCreateView(LoginRequiredMixin,CreateView):
    template_name = "product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("products:product_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user).exists()
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if vendor and user.vendor.status == Vendor.VendorStatus.SUSPENDED:
                return redirect ("vendor:vendor_dashboard")
            if vendor and user.vendor.status in [Vendor.VendorStatus.REJECTED,Vendor.VendorStatus.PENDING]:
                return redirect ("vendor:vendor_detail")
            if not vendor:
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "product_form.html"
    form_class = ProductForm
    success_url = reverse_lazy("products:product_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user).exists()
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if vendor and user.vendor.status in [Vendor.VendorStatus.REJECTED,Vendor.VendorStatus.PENDING]:
                return redirect ("vendor:vendor_detail")
            if not vendor:
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    

class ProductDetailView(LoginRequiredMixin,DetailView):
    template_name = "product_detail.html"
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user).exists()
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if vendor and user.vendor.status in [Vendor.VendorStatus.REJECTED,Vendor.VendorStatus.PENDING]:
                return redirect ("vendor:vendor_detail")
            if not vendor:
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    
class ProductDeleteView(LoginRequiredMixin,DeleteView):
    success_url = reverse_lazy("products:product_list")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user).exists()
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if vendor and user.vendor.status in [Vendor.VendorStatus.REJECTED,Vendor.VendorStatus.PENDING]:
                return redirect ("vendor:vendor_detail")
            if not vendor:
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    
