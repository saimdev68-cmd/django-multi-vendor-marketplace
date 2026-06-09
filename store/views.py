from django.shortcuts import render
from django.views.generic import TemplateView , ListView
from products.models import Category , Product , Vendor
from django.db.models import Q

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["products"] = Product.objects.all()[:4]
        context["vendors"] = Vendor.objects.all()
        return context
    
class SearchView(ListView):
    template_name = "search.html"
    context_object_name = "products"
    paginate_by = 30

    def get_queryset(self):
        q = self.request.GET.get("q")
        return Product.objects.filter(Q(name__icontains=q)|Q(category__name__icontains=q))
    