"""
URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from services.views import ServicioViewSet, SolicitudClienteViewSet

# Router para ViewSets
router = DefaultRouter()
router.register(r'servicios', ServicioViewSet, basename='servicio')
router.register(r'solicitudes', SolicitudClienteViewSet, basename='solicitud')


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint simple.
    GET /api/health
    """
    return Response({'status': 'ok'}, status=status.HTTP_200_OK)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health', health_check, name='health-check'),
    path('api/', include(router.urls)),
]


