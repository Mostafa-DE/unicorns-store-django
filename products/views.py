from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializer import ProductSerializer


class ProductsCategoryView(APIView):
    @staticmethod
    def get(request, category):
        products = Product.objects.filter(category__slug=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(APIView):
    @staticmethod
    def get(request, category, slug):
        try:
            product = Product.objects.get(category__slug=category, slug=slug)
            serializer = ProductSerializer(product)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)
