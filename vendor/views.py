from django.views.generic import DetailView , TemplateView , UpdateView 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vendor 
from .forms import VendorForm 
from bank_account.forms import BankAccountForm
from django.shortcuts import render , redirect
from django.urls import reverse_lazy

class VendorCreateView(LoginRequiredMixin,View):
    template_name = "vendor_create.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home") 
        if Vendor.objects.filter(owner=user).exclude():
            if user.vendor.status in [Vendor.VendorStatus.ACTIVE ,Vendor.VendorStatus.SUSPENDED]:
                return redirect ("vendor:dashboard")
            else:
                return redirect ("vendor:vendor_detail")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request):
        vendor_form = VendorForm()
        bank_account_form = BankAccountForm()
        return render (request,self.template_name,{
            "vendor_form":vendor_form,
            "bank_account_form":bank_account_form
        })
    
    def post(self,request):
        vendor_form = VendorForm(request.POST)
        bank_account_form = BankAccountForm(request.POST)
        if vendor_form.is_valid() and bank_account_form.is_valid():
            vendor = vendor_form.save(commit=False)
            vendor.owner = request.user
            vendor.save()
            bank_account = bank_account_form.save(commit=False)
            bank_account.vendor = vendor
            bank_account.save()
            return redirect ("vendor:vendor_detail")
        return render (request,self.template_name,{
            "vendor_form":vendor_form,
            "bank_account_form":bank_account_form
        })
    

class VendorDetailView(LoginRequiredMixin,DetailView):
    template_name = "vendor_detail.html"
    context_object_name = "vendor"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if not Vendor.objects.filter(owner=user).exists():
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return Vendor.objects.get(owner=self.request.user)
    
class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = "vendor_update.html"
    success_url = reverse_lazy("vendor:vendor_detail")

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        if user.is_vendor:
            if not Vendor.objects.filter(owner=user).exists():
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return Vendor.objects.get(owner=self.request.user)
    

class VendorDashboardView(LoginRequiredMixin,TemplateView):
    template_name = "vendor_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user).exists()
        if not user.is_vendor :
            return redirect ("store:home")
        if user.is_vendor:
            if vendor and user.vendor.status not in [Vendor.VendorStatus.ACTIVE,Vendor.VendorStatus.SUSPENDED]:
                return redirect ("vendor:vendor_detail")
            if not vendor:
                return redirect ("vendor:vendor_create")
        return super().dispatch(request, *args, **kwargs)