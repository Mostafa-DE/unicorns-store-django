from django.urls import path, include

urlpatterns = [
    path('cart/', include('purchasing.cart.urls'), name='cart'),
]
