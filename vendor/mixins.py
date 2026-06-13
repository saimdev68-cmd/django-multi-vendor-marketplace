from django.shortcuts import redirect
from .models import Vendor

class IsVendorMixin:

    def dispatch(self,request,*args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        return super().dispatch(request,*args, **kwargs)
    
class VendorStoreMixin(IsVendorMixin):

    def dispatch(self,request,*args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user)
        if vendor:
            if vendor.status in [Vendor.VendorStatus.ACTIVE,Vendor.VendorStatus.SUSPENDED]:
                return redirect ("vendor:dashboard")
            else:
                return redirect ("vendor:detail")
        return super().dispatch(request,*args, **kwargs)
    
class VendorSetupMixin(IsVendorMixin):

    def dispatch(self,request,*args, **kwargs):
        user = request.user
        vendor = Vendor.objects.filter(owner=user)
        if not vendor:
            return redirect ("vendor:setup")
        return super().dispatch(request,*args, **kwargs)
        
class VendorSetupRequiredMixin(VendorStoreMixin):
    pass

class VendorDetailRequiredMixin(VendorSetupMixin):
    pass