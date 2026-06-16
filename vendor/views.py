from django.views.generic import DetailView , TemplateView , UpdateView 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Vendor , City
from django.http import JsonResponse
from .forms import VendorForm 
from bank_account.forms import BankAccountForm
from django.shortcuts import render , redirect
from django.urls import reverse_lazy
from .services.setup_service import VendorSetupService
from .mixins import VendorSetupRequiredMixin  , VendorDetailRequiredMixin , VendorDashboardRequiredMixin 
from products.models import Product
from django.db.models import Count , Q , Sum , F , DecimalField
from order.models import OrderItem
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, Sum, Count, Q, DecimalField
from django.db.models.functions import TruncDay, Coalesce
from decimal import Decimal

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
    
class VendorDashboardView(LoginRequiredMixin, VendorDashboardRequiredMixin, TemplateView):
    template_name = "vendor_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.request.user.vendor
        now = timezone.now()
        
        # Time boundary marks
        seven_days_ago = now - timedelta(days=7)
        twenty_eight_days_ago = now - timedelta(days=28)

        # 1. Base Querysets
        products = Product.objects.filter(vendor=vendor)
        order_items = OrderItem.objects.filter(vendor=vendor)

        # Reusable Type Definition to keep queries DRY and matching database schema
        money_field = DecimalField(max_digits=12, decimal_places=2)
        decimal_zero = Decimal('0.00')

        # 2. Complete Lifetime Portfolio Metrics Matrix (FIXED COALESCE & ARGS MATCH)
        all_time_metrics = order_items.aggregate(
            # All-Time Totals
            total_sales=Coalesce(
                Sum(F('price') * F('quantity'), output_field=money_field), 
                decimal_zero, 
                output_field=money_field
            ),
            total_orders=Count('order', distinct=True),
            
            # Past 7 Days metrics
            sales_7_days=Coalesce(
                Sum(F('price') * F('quantity'), filter=Q(order__created_at__gte=seven_days_ago), output_field=money_field), 
                decimal_zero, 
                output_field=money_field
            ),
            orders_7_days=Count('order', distinct=True, filter=Q(order__created_at__gte=seven_days_ago)),
            
            # Past 28 Days metrics
            sales_28_days=Coalesce(
                Sum(F('price') * F('quantity'), filter=Q(order__created_at__gte=twenty_eight_days_ago), output_field=money_field), 
                decimal_zero, 
                output_field=money_field
            ),
            orders_28_days=Count('order', distinct=True, filter=Q(order__created_at__gte=twenty_eight_days_ago))
        )

        # 3. Product Catalog Metrics
        product_counts = products.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status=Product.ProductStatus.ACTIVE))
        )

        # 4. Generate Day-by-Day Historical Chart Pipelines
        daily_stats = order_items.filter(order__created_at__gte=twenty_eight_days_ago) \
            .annotate(day=TruncDay('order__created_at')) \
            .values('day') \
            .annotate(
                sales=Coalesce(Sum(F('price') * F('quantity'), output_field=money_field), decimal_zero, output_field=money_field),
                orders=Count('order', distinct=True)
            ) \
            .order_by('day')

        # Organize database dictionary datasets into sequential arrays for frontend charts
        chart_data_28 = {
            "labels": [stat['day'].strftime('%b %d') for stat in daily_stats],
            "sales": [float(stat['sales']) for stat in daily_stats],
            "orders": [stat['orders'] for stat in daily_stats]
        }

        # Slice the last 7 data rows for the shorter charts
        chart_data_7 = {
            "labels": chart_data_28["labels"][-7:],
            "sales": chart_data_28["sales"][-7:],
            "orders": chart_data_28["orders"][-7:]
        }

        # 5. Fallback Math & Operational Parameters
        total_sales_val = float(all_time_metrics['total_sales'])
        total_orders_val = all_time_metrics['total_orders']
        avg_sales = (total_sales_val / total_orders_val) if total_orders_val > 0 else 0.00

        # 6. Bind to Template Context Dictionary
        context["metrics"] = {
            "total_products": product_counts['total'],
            "active_products": product_counts['active'],
            "review_rating": 4.8,
            "available_balance": 0.00,
            "avg_sales_value": avg_sales,
            
            # All-Time Totals
            "total_sales": total_sales_val,
            "total_orders": total_orders_val,
            
            # Periodic Breakdowns
            "sales_7_days": float(all_time_metrics['sales_7_days']),
            "orders_7_days": all_time_metrics['orders_7_days'],
            "sales_28_days": float(all_time_metrics['sales_28_days']),
            "orders_28_days": all_time_metrics['orders_28_days'],
        }

        # Chart datasets passed as clean JSON-friendly dictionaries
        context["chart_data_7"] = chart_data_7
        context["chart_data_28"] = chart_data_28

        return context
    
def load_cities_ajax(request):
    country_id = request.GET.get('country_id')
    if country_id:
        # Fetch only active cities belonging to the selected country
        cities = City.objects.filter(
            country_id=country_id, 
            is_active=True
        ).order_by("name").values("id", "name")
        
        return JsonResponse(list(cities), safe=False)
        
    return JsonResponse([], safe=False)