from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import OrderSerializer

from products.models import Product
from purchasing.order.models import Order
from ..cart.models import Cart


class OrderView(APIView):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(
                {'error': "No orders found, consider to login first to save your orders"},
                status=status.HTTP_404_NOT_FOUND
            )

        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        data = request.data
        order = Order.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            address=data['address'],
            phone=data['phone'],
            city=data['city'],
            building_number=data['building_number'],
            order_number=data['order_number'],
            additional_info=data['additional_info'],
        )
        for item in data['cart_items']:
            product = Product.objects.get(id=item['product_id'])
            order.order_lines.create(
                order=order,
                product=product,
                quantity=item['quantity']
            )
            product.stock -= item['quantity']
            product.save()

        if request.user.id:
            order.user = request.user
            order.save()
            cart = Cart.objects.get(user=request.user)
            cart.cart_items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
