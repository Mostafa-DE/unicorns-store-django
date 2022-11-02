from django.urls import path, include

urlpatterns = [
    path('cart/', include('purchasing.cart.urls'), name='cart'),
    path('orders/', include('purchasing.order.urls'), name='orders'),
]
