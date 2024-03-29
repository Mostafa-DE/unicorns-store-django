from django.contrib import admin
from django.urls import path, include
from core import settings
from django.conf.urls.static import static
from main.views import main

urlpatterns = [
    path('', main, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('products.urls')),
    path('api/', include('purchasing.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
