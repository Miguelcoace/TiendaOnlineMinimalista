from django.views.generic import TemplateView, CreateView
from catalog.models import Category, Product
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = "_core/_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all().order_by('name')

        products = Product.objects.all().order_by('-created_at')[:3]

        context['categories'] = categories
        context['products'] = products

        return context

class SignUpView(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy('login')  # Tras registrarse, va al login
  template_name = '_core/_signup.html'

class legalView(TemplateView):
    template_name = '_core/_legal.html'