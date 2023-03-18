from rest_framework import serializers
from .models import Product, ProductAttribute, ProductSize, ProductImage, ProductVideo


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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

    def to_representation(self, instance):
        return {
            'url': instance.image.url,
        }


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ['video']

    def to_representation(self, instance):
        return {
            'url': instance.video.url,
            'image': instance.video.video_thumbnail(),
        }


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    attributes = AttributeSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'slug',
            'description',
            'images',
            'videos',
            'sizes',
            'attributes',
            'price',
            'stock',
            'available',
            'pre_order',
            'made_in',
            'discount_percentage',
            'created',
            'updated',
        ]
