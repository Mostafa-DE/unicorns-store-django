from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import Cart, CartItem
from .serializer import CartSerializer, CartItemSerializer


@permission_classes((IsAuthenticated,))
class CartView(APIView):
    @staticmethod
    def get(request):
        cart = Cart.objects.get_or_create(user=request.user)[0]
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemView(APIView):
    @staticmethod
    def post(request):
        try:
            product = Product.objects.get(id=request.data['product'])
            quantity = request.data.get('quantity')
            cart_item = CartItem.objects.filter(product=product, cart__user=request.user)
            if cart_item.exists():
                cart_item = cart_item[0]
                cart_item.quantity += 1
                cart_item.save()
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                cart = Cart.objects.get(user=request.user)
                cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                serializer = CartItemSerializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, id=request.data['id'])
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)
