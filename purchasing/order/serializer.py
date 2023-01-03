from rest_framework import serializers
from .models import Order, OrderLine
from products.serializer import ProductSerializer
from users.serializer import UserSerializer


class OrderLinesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderLine
        fields = ('id', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order_lines = OrderLinesSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField('get_total')

    @staticmethod
    def get_total(obj):
        return obj.get_total()

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'order_lines',
            'first_name',
            'last_name',
            'email',
            'address',
            'phone',
            'city',
            'order_number',
            'is_delivered',
            'additional_info',
            'total',
            'created_at',
        )
