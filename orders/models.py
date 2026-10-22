from catalog.models import Product
from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  paid = models.BooleanField(default=False)  # Útil para la pasarela de pago simulada
  status = models.CharField(
      max_length=20,
      choices=[
          ('pending', 'Pendiente'),
          ('processing', 'En proceso'),
          ('shipped', 'Enviado'),
          ('delivered', 'Entregado'),
      ],
      default='pending',
  )

  class Meta:
    ordering = ['-created_at']

  def __str__(self):
    return f'Pedido #{self.id} - {self.user.username}'

  @property
  def get_total_cost(self):
    return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
  order = models.ForeignKey(
      Order, related_name='items', on_delete=models.CASCADE
  )
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  price = models.DecimalField(
      max_digits=10, decimal_places=2
  )  # Precio histórico en el momento de la compra
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return f'{self.quantity}x {self.product.name}'

  def get_cost(self):
    return self.price * self.quantity