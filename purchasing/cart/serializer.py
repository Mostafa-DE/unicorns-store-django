from rest_framework import serializers
from .models import Cart, CartItem
from products.serializer import ProductSerializer
from users.serializer import UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    cart_total = serializers.IntegerField(source='get_cart_total')

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'cart_total', 'size', 'color')


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart_items = CartItemSerializer(many=True, read_only=True)
    cart_total = serializers.IntegerField(source='get_cart_total')

    class Meta:
        model = Cart
        fields = ('id', 'user', 'cart_items', 'cart_total', 'created_at', 'updated_at')
