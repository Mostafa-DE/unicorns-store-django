from _decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_cart_total(self):
        total = 0
        for item in self.cart_items.all():
            total += item.get_total_line()
        return Decimal(total)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product', unique=False)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=4, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    def get_total_line(self):
        return self.product.price * self.quantity

    def get_cart_total(self):
        return self.cart.get_cart_total()

    def __str__(self):
        return f"{self.cart.user.username} - {self.product.name}"
