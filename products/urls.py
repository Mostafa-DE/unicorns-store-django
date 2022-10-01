from django.urls import path
from .views import ProductsCategoryView, ProductView

urlpatterns = [
    path('<slug:category>/products/', ProductsCategoryView.as_view(), name='products'),
    path('<slug:category>/products/<slug:slug>/', ProductView.as_view(), name='product'),
]
