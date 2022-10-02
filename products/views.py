from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializer import ProductSerializer


class ProductsCategoryView(APIView):
    @staticmethod
    def get(request, category):
        products = Product.objects.filter(category__slug=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)


class ProductView(APIView):
    @staticmethod
    def get(request, category, slug):
        product = Product.objects.get(category__slug=category, slug=slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)
