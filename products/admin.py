from django.contrib import admin
from .models import Category, Product, ProductImage, ProductVideo, ProductAttribute, ProductSize

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(ProductVideo)
admin.site.register(ProductAttribute)
admin.site.register(ProductSize)
