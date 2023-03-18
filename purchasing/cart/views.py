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
            product_id = request.data.get('productId')
            product = Product.objects.get(id=product_id)
            quantity = request.data.get('quantity')
            color = request.data.get('color')
            size = request.data.get('size')
            user = request.user
            cart_item = CartItem.objects.filter(product=product, cart__user=user)
            if cart_item.exists():
                if color:
                    cart_item = cart_item.filter(color=color)

                if size:
                    cart_item = cart_item.filter(size=size)

                if cart_item.exists():
                    cart_item = cart_item.first()
                    cart_item.quantity += 1
                    cart_item.save()
                    serializer = CartItemSerializer(cart_item)
                    return Response(serializer.data, status=status.HTTP_200_OK)

            cart = Cart.objects.get(user=user)
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                color=color,
                size=size
            )
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def put(request, pk):
        try:
            qty = request.data.get('qty')
            if qty < 1:
                CartItem.objects.get(id=pk).delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)

            cart_item = CartItem.objects.get(cart__user=request.user, id=pk)
            cart_item.quantity = qty
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete(request, pk):
        try:
            cart_item = CartItem.objects.get(cart__user=request.user, id=pk)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item does not exist'}, status=status.HTTP_404_NOT_FOUND)
