from django.shortcuts import redirect
from .models import Vendor

class IsVendor:

    def dispatch(self,request,*args, **kwargs):
        user = request.user
        if not user.is_vendor:
            return redirect ("store:home")
        return super().dispatch(request,*args, **kwargs)
    
class VendorMixin(IsVendor):
    def get_vendor(self):
        if not hasattr(self.request,'_vendor_cache'):
            self.request._vendor_cache = Vendor.objects.select_related('owner','city','country').filter(owner_id=self.request.user.id).first()
        return self.request._vendor_cache
    
class VendorStatus(IsVendor):
    def dispatch(self,request,*args, **kwargs):
        user = request.user
        if user.vendor.status in [Vendor.Status.PENDING,Vendor.Status.REJECTED]:
            return redirect ("vendor:detail")
        return super().dispatch(request,*args, **kwargs)
    
class VendorSetupRequiredMixin(VendorMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_vendor():
            return redirect ("vendor:detail")
        return super().dispatch(request, *args, **kwargs)

class VendorDetailRequiredMixin(VendorMixin):

    def dispatch(self, request, *args, **kwargs):
        if not self.get_vendor():
            return redirect ("vendor:setup")
        return super().dispatch(request, *args, **kwargs)

class VendorDashboardRequiredMixin(VendorStatus):
    pass