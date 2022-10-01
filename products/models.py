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
    product_images = models.ForeignKey(
        'ProductImage',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='product_images'
    )
    attributes = models.ManyToManyField('ProductAttribute', related_name='product_attributes', blank=True)
    size = models.ManyToManyField('ProductSize', related_name='product_size', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
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
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='images')
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.product.name


class ProductSize(models.Model):
    size = models.CharField(max_length=50)

    def __str__(self):
        return self.size
