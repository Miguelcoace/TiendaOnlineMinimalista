from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category

from django.shortcuts import get_object_or_404


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "catalog/_product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all().order_by('name')

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/_product_detail.html"
    context_object_name = "product"


class CategoryListView(ListView):
    model = Category
    template_name = "catalog/_category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.all().order_by('name')

class ProductByCategoryListView(ListView):
  model = Product
  template_name = 'catalog/_product_list.html'
  context_object_name = 'products'
  paginate_by = 10  # Opcional: paginación por si hay muchos productos

  def get_queryset(self):
    # 1. Busca la categoría por su slug (o da error 404 si no existe)
    self.category = get_object_or_404(
        Category, slug=self.kwargs['category_slug']
    )
    # 2. Filtra los productos que pertenecen exclusivamente a esta categoría
    return Product.objects.filter(category=self.category, available=True)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # 3. Inyectamos la categoría actual en el contexto para mostrar su título en el HTML
    context['category'] = self.category
    return context