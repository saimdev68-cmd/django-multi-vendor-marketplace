from django.shortcuts import render , redirect
from django.views.generic import ListView , CreateView , UpdateView , DeleteView , DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product 
from .forms import ProductForm
from vendor.models import Vendor
from django.urls import reverse_lazy
from django.db.models import Q

class ProductListView(LoginRequiredMixin,ListView):
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 30

    def get_queryset(self):
        queryset = Product.objects.filter(
            vendor=self.request.user.vendor
        ).select_related('category')
        self.search_query = self.request.GET.get('q', '').strip()
        self.status_filter = self.request.GET.get('status', '').strip()
        self.stock_filter = self.request.GET.get('stock', '').strip()
        if self.search_query:
            queryset = queryset.filter(
                Q(name__icontains=self.search_query) | 
                Q(sku__iexact=self.search_query)
            )
        if self.status_filter in Product.ProductStatus.values:
            queryset = queryset.filter(status=self.status_filter)
        
        if self.stock_filter == 'out_of_stock':
            queryset = queryset.filter(stock=0)
        elif self.stock_filter == 'low_stock':
            queryset = queryset.filter(stock__gt=0, stock__lte=5)

        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Persists current search state variables directly into the template context 
        to ensure filters don't break during active pagination links.
        """
        context = super().get_context_data(**kwargs)
        
        # Keep track of filter states within input search boxes
        context['current_search'] = self.search_query
        context['current_status'] = self.status_filter
        context['current_stock'] = self.stock_filter
        
        # Expose Status Options list directly to populate custom filter select dropdowns
        context['status_choices'] = Product.ProductStatus.choices
        
        return context
    
class ProductCreateView(LoginRequiredMixin,CreateView):
    template_name = "product_form.html"
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("products:list")

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        return super().form_valid(form)
    
class ProductUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "product_form.html"
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy("products:list")
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    

class ProductDetailView(LoginRequiredMixin,DetailView):
    template_name = "product_detail.html"
    context_object_name = "product"
    model = Product
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)
    
class ProductDeleteView(LoginRequiredMixin,DeleteView):
    model = Product
    success_url = reverse_lazy("products:list")
    
    def get_queryset(self):
        return Product.objects.filter(vendor=self.request.user.vendor)