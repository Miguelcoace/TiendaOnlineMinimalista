"""
URL configuration for TiendaOnlineMinimalista project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import HomeView,  legalView, SignUpView
from catalog.views import ProductListView, ProductDetailView, CategoryListView, ProductByCategoryListView
from django.urls import include 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('productos/', ProductListView.as_view(), name='products'),
    path('producto/<slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('categorias/', CategoryListView.as_view(), name='categories'),
    path('categoria/<slug:category_slug>/', ProductByCategoryListView.as_view(), name='category_products'),
    path('carrito/', include('cart.urls'), name='cart_detail'),
    path('orders/', include('orders.urls'), name="order_create"),

    path('login/',auth_views.LoginView.as_view(template_name='_core/_login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('legal/', legalView.as_view(), name='legal'),
    path('admin/', admin.site.urls),
]
