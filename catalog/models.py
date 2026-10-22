from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='TiendaOnlineMinimalista/img/categories', blank=True, null=True
    )  

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']  # Ordenar alfabéticamente por defecto

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
      Category, related_name='products', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']  # Los productos más recientes aparecen primero
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]


    def __str__(self):
        return self.name