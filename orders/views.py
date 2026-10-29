from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .forms import PaymentForm
from django.contrib.admin.views.decorators import staff_member_required

class OrderListView(LoginRequiredMixin, ListView):
  model = Order
  template_name = 'order/_order_list.html'
  context_object_name = 'orders'
  login_url = 'login'

  def get_queryset(self):
    # Solo devuelve los pedidos del usuario que ha iniciado sesión, ordenados del más reciente al más antiguo
    return Order.objects.filter(user=self.request.user).order_by('-created_at')

@login_required(login_url='login')
def order_create(request):
  cart = Cart(request)
  if not cart.cart:
    return redirect('cart_detail')

  if request.method == 'POST':
    # 1. Crear la cabecera del pedido
    order = Order.objects.create(user=request.user, paid=False)

    # 2. Crear los ítems del pedido y restar stock
    for item in cart:
      product = item[
          'product'
      ]  # Esto viene del iterador, es correcto usarlo aquí
      OrderItem.objects.create(
          order=order,
          product=product,
          price=item['price'],
          quantity=item['quantity'],
      )
      product.stock -= item['quantity']
      product.save()

    # 3. GUARDAR SOLO EL ID (Entero -> 100% JSON serializable)
    request.session['order_id'] = order.id

    # 4. (Opcional por seguridad) Limpiamos los datos del carrito viejo de la sesión
    # para evitar que arrastre instancias de productos
    del request.session['cart']
    request.session.modified = True

    return redirect('payment_process')

  return render(request, '_core/_checkout.html', {'cart': cart})



@login_required(login_url='login')
def payment_process(request):
  order_id = request.session.get('order_id')
  order = get_object_or_404(Order, id=order_id)

  if request.method == 'POST':
    form = PaymentForm(request.POST)
    if form.is_valid():
      # Simulamos que el pago se aprueba con éxito
      order.paid = True
      order.status = 'processing'  # Cambiamos el estado a en proceso
      order.save()

      # Limpiamos el carrito de la sesión y el order_id temporal
      cart = Cart(request)
      cart.clear()
      if 'order_id' in request.session:
        del request.session['order_id']

      return render(request, 'order/_order_created.html', {'order': order})
  else:
    form = PaymentForm()

  return render(
      request, 'order/_payment.html', {'order': order, 'form': form}
  )

@staff_member_required(login_url='login')
def staff_order_list(request):
  # El staff puede ver todos los pedidos del sistema, ordenados del más reciente al más antiguo
  orders = Order.objects.all().order_by('-created_at')
  return render(request, 'order/_staff_order_list.html', {'orders': orders})

@staff_member_required(login_url='login')
def staff_order_update_status(request, order_id):
  order = get_object_or_404(Order, id=order_id)

  if request.method == 'POST':
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
      order.status = new_status
      order.save()
  return redirect('staff_order_list')