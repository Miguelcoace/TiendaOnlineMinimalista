from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('history/', views.OrderListView.as_view(), name='order_list'),
    path('payment/', views.payment_process, name='payment_process'),
]