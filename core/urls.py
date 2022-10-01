from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core import settings
from django.conf.urls.static import static


class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        return Response({'message': 'Hello, World!'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('products.urls')),
    path('hello/', ProtectedView.as_view(), name='hello'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
