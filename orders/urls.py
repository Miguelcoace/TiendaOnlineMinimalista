from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('history/', views.OrderListView.as_view(), name='order_list'),
    path('payment/', views.payment_process, name='payment_process'),
    path('staff/orders/', views.staff_order_list, name='staff_order_list'),
    path('staff/orders/<int:order_id>/update/',views.staff_order_update_status,name='staff_order_update_status',),
]