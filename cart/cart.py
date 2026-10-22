from decimal import Decimal
from catalog.models import Product


class Cart:

    def __init__(self, request):
      """Inicializa el carrito de compras usando la sesión."""
      self.session = request.session
      cart = self.session.get('cart')
      if not cart:
        # Si el usuario no tiene carrito en la sesión, creamos uno vacío
        cart = self.session['cart'] = {}
      self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
      """Añade un producto al carrito usando su ID para evitar problemas."""
      product_id = str(product.id)  # Usamos el ID como clave (¡mucho más seguro!)

      if product_id not in self.cart:
        self.cart[product_id] = {
            'quantity': 0,
            'price': str(product.price),
        }

      if override_quantity:
        self.cart[product_id]['quantity'] = quantity
      else:
        self.cart[product_id]['quantity'] += quantity

      self.save()

    def save(self):
      """Marca la sesión como modificada para que Django la guarde."""
      self.session.modified = True

    def remove(self, product):
      """Elimina un producto del carrito."""
      product_name = str(product.name)
      if product_name in self.cart:
        del self.cart[product_name]
        self.save()

    def __iter__(self):
      """Recorre los elementos del carrito buscando los productos por ID."""
      product_ids = self.cart.keys()
      products = Product.objects.filter(id__in=product_ids)

      # Creamos una copia de los datos de la sesión para no alterar el original
      cart = self.cart.copy()

      for product in products:
        # Añadimos el objeto product temporalmente SOLO para la iteración/plantilla
        cart[str(product.id)]['product'] = product

      for item in cart.values():
        # Creamos una copia limpia del item para operar con Decimal sin tocar la sesión
        cart_item = item.copy()
        cart_item['price'] = Decimal(item['price'])
        cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
        yield cart_item

    def get_total_price(self):
      """Calcula el precio total de todos los productos en el carrito."""
      return sum(
          Decimal(item['price']) * item['quantity'] for item in self.cart.values()
      )

    def clear(self):
        """Vacía el carrito de la sesión."""
        del self.session['cart']
        self.save()

    def __len__(self):
      """Cuenta todos los artículos sumando sus cantidades en el carrito."""
      return sum(item['quantity'] for item in self.cart.values())