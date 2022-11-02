from rest_framework import serializers
from .models import Cart, CartItem
from products.serializer import ProductSerializer
from users.serializer import UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items', 'created_at', 'updated_at')
