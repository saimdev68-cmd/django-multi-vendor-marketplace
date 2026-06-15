from django.views.generic import DetailView , TemplateView , UpdateView 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vendor 
from .forms import VendorForm 
from bank_account.forms import BankAccountForm
from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from .services.setup_service import VendorSetupService
from .mixins import VendorSetupRequiredMixin  , VendorDetailRequiredMixin , VendorDashboardRequiredMixin 

class VendorSetupView(LoginRequiredMixin,VendorSetupRequiredMixin,View):
    template_name = "setup_profile.html"
    
    def get(self,request):
        return render (request,self.template_name,{
            "vendor_form":VendorForm(),
            "bank_account_form":BankAccountForm()
        })
    
    def post(self,request):
        vendor , vendor_form , bank_account_form = VendorSetupService.create_vendor_with_bank(
            user=request.user,
            post_data=request.POST,
            file_data=request.FILES
        )
        if vendor:
            return redirect ("vendor:detail")
        
        return render (request,self.template_name,{
            "vendor_form":vendor_form,
            "bank_account_form":bank_account_form
        })
    

class VendorDetailView(LoginRequiredMixin,VendorDetailRequiredMixin,DetailView):
    model = Vendor
    template_name = "vendor_detail.html"
    context_object_name = "vendor"

    def get_object(self, queryset=None):
        return self.get_vendor()
    
class VendorUpdateView(LoginRequiredMixin,VendorDetailRequiredMixin,UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = "vendor_update.html"
    success_url = reverse_lazy("vendor:detail")

    def get_object(self, queryset=None):
        return self.get_vendor()
    

class VendorDashboardView(LoginRequiredMixin,VendorDashboardRequiredMixin,TemplateView):
    template_name = "vendor_dashboard.html"