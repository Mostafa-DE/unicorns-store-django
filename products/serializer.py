from rest_framework import serializers
from .models import Product, ProductAttribute, ProductSize


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['name', 'value']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('size',)


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    attributes = AttributeSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'slug',
            'description',
            'product_images',
            'size',
            'attributes',
            'price',
            'stock',
            'available',
            'pre_order',
            'made_in',
            'sale_percentage',
            'created',
            'updated',
        ]

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = ProductCategorySerializer.create(ProductCategorySerializer(), validated_data=category_data)
        product = Product.objects.create(category=category, **validated_data)
        return product
