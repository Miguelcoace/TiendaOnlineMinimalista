from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'image')
    search_fields = ('name', 'slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price','stock', 'available', 'created_at', 'image')
    search_fields = ('name', 'category', 'available', 'created_at')