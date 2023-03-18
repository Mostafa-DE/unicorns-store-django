from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializer import ProductSerializer


@permission_classes((AllowAny,))
class ProductsCategoryView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request, category):
        try:
            products = Product.objects.filter(category__slug=category)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ProductView(APIView):
    authentication_classes = []

    @staticmethod
    def get(request, category, slug):
        try:
            product = Product.objects.get(category__slug=category, slug=slug)
            serializer = ProductSerializer(product)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)
