from django.views.generic import TemplateView , ListView
from products.models import Category , Product , Vendor
from django.db.models import Q

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()[:5]
        context["products"] = Product.objects.all()[:4].select_related("vendor")
        context["vendors"] = Vendor.objects.all()[:4]
        return context
    
class CategoryListView(ListView):
    template_name = "category_list.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        return Category.objects.all()
    

class ProductListView(ListView):
    template_name = "list.html"
    context_object_name = "products"
    paginate_by = 30

    def get_queryset(self):
        return Product.objects.all()
    
class VendorListView(ListView):
    template_name = "vendor.html"
    context_object_name = "vendors"
    paginate_by = 10

    def get_queryset(self):
        return Vendor.objects.all()

    
class SearchView(ListView):
    template_name = "list.html"
    context_object_name = "products"
    paginate_by = 30

    def get_queryset(self):
        q = self.request.GET.get("q")
        return Product.objects.filter(Q(name__icontains=q)|Q(category__name__icontains=q))
    