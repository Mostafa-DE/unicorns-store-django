from django.urls import path
from .views import CartView, CartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('item/', CartItemView.as_view(), name='cart_items'),
    path('item/<int:pk>/', CartItemView.as_view(), name='cart_items'),
]
