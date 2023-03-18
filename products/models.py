from cloudinary.models import CloudinaryField
from django.db import models
from .helpers import unique_slugify
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    description = models.TextField(blank=True)
    sizes = models.ManyToManyField('ProductSize', related_name='product_size', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    pre_order = models.BooleanField(default=False)
    made_in = models.CharField(max_length=50, blank=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='attributes')
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} - {self.value} - {self.product.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.image.url


class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='videos')
    video = CloudinaryField('video', null=True, blank=True, resource_type='video')

    def __str__(self):
        return self.video.url


class ProductSize(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size
