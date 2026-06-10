from django.views.generic import DetailView , TemplateView , UpdateView , ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vendor , BankAccount
from .form import VendorForm , BankAccountForm
from django.shortcuts import render , redirect
from django.urls import reverse_lazy

class VendorCreateView(LoginRequiredMixin,View):
    template_name = "vendor_create.html"

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        if Vendor.objects.filter(owner=user).exclude():
            if user.vendor.is_verified:
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
    

class VendorDashboardView(LoginRequiredMixin,TemplateView):
    template_name = "vendor_dashboard.html"



    def get(self,request):
        vendor_form = VendorForm()
        bank_account_form = BankAccountForm()
        return render (request,"vendor_create.html",{
            "vendor_form":vendor_form,
            "bank_account_form":bank_account_form
        })
    
    def post(self,request):
        vendor_form = VendorForm(request.POST,request.FILES)
        bank_account_form = BankAccountForm(request.POST)
        if vendor_form.is_valid() and bank_account_form.is_valid():
            vendor = vendor_form.save(commit=False)
            bank_account = bank_account_form.save(commit=False)
            vendor.owner = request.user
            vendor.save()
            bank_account.vendor = vendor
            bank_account.save()
            return redirect ("vendor:vendor_dashboard")
        return render (request,"vendor_create.html",{
            "vendor_form":vendor_form,
            "bank_account_form":bank_account_form
        })
    
class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = "vendor_edit.html"
    success_url = reverse_lazy("vendor:vendor_detail")

    def get_object(self):
        return self.request.user.vendor
    
class BankAccountListView(LoginRequiredMixin,ListView):
    template_name = "bank_list.html"
    context_object_name = "bank_accounts"

    def get_queryset(self):
        return BankAccount.objects.filter(vendor=self.request.user.vendor)
    
class BankAccountDetailView(LoginRequiredMixin, DetailView):
    model = BankAccount
    template_name = "bank_detail.html"
    context_object_name = "bank"

    def get_queryset(self):
        return BankAccount.objects.filter(vendor=self.request.user.vendor)
    
class BankAccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BankAccountForm
    template_name = "bank_form.html"
    success_url = reverse_lazy("vendor:bank_list")

    def get_queryset(self):
        return BankAccount.objects.filter(vendor=self.request.user.vendor)