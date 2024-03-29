from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from ..cart.models import Cart
from products.models import Product

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    building_number = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    order_number = models.CharField(max_length=20, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    additional_info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        total = 0
        for line in self.order_lines.all():
            total += line.get_total_line()
        return Decimal(total)

    def __str__(self):
        if self.user:
            return f'{self.user.username} - {self.order_number}'
        return f'[Anonymous] {self.first_name} {self.last_name} - {self.order_number}'


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_lines', unique=False)
    quantity = models.PositiveIntegerField()

    def get_total_line(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.order.first_name} - {self.product.name}"
