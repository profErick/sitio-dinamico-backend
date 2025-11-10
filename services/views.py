from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from django.db import models

from .models import Servicio, SolicitudCliente
from .serializers import (
    ServicioSerializer,
    SolicitudClienteSerializer,
    SolicitudClienteNestedSerializer
)
from .filters import ServicioFilter, SolicitudClienteFilter


class ServicioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo Servicio.
    
    Permite CRUD completo con filtros, búsqueda y ordenación.
    """
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [AllowAny]  # En producción, usar permisos apropiados
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServicioFilter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio_mxn', 'fecha_publicacion', 'nombre']
    ordering = ['-fecha_publicacion']

    def get_queryset(self):
        """
        Permite filtrado adicional por parámetros de query.
        """
        queryset = super().get_queryset()
        
        # Aplicar filtros personalizados
        categoria = self.request.query_params.get('categoria', None)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        activo = self.request.query_params.get('activo', None)
        if activo is not None:
            activo_bool = activo.lower() in ('true', '1', 'yes')
            queryset = queryset.filter(activo=activo_bool)
        
        min_precio = self.request.query_params.get('min_precio', None)
        if min_precio:
            try:
                queryset = queryset.filter(precio_mxn__gte=float(min_precio))
            except ValueError:
                pass
        
        max_precio = self.request.query_params.get('max_precio', None)
        if max_precio:
            try:
                queryset = queryset.filter(precio_mxn__lte=float(max_precio))
            except ValueError:
                pass
        
        # Búsqueda por nombre o descripción
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(nombre__icontains=search) |
                models.Q(descripcion__icontains=search)
            )
        
        # Ordenación
        ordenar_por = self.request.query_params.get('ordenar_por', None)
        if ordenar_por == 'precio_asc':
            queryset = queryset.order_by('precio_mxn')
        elif ordenar_por == 'precio_desc':
            queryset = queryset.order_by('-precio_mxn')
        elif ordenar_por == 'fecha_asc':
            queryset = queryset.order_by('fecha_publicacion')
        elif ordenar_por == 'fecha_desc':
            queryset = queryset.order_by('-fecha_publicacion')
        
        return queryset

    @action(detail=True, methods=['get', 'post'], url_path='solicitudes')
    def solicitudes(self, request, pk=None):
        """
        Endpoint anidado para obtener o crear solicitudes de un servicio.
        
        GET /api/servicios/{id}/solicitudes - Lista solicitudes del servicio
        POST /api/servicios/{id}/solicitudes - Crea una solicitud para el servicio
        """
        servicio = self.get_object()
        
        if request.method == 'GET':
            solicitudes = servicio.solicitudes.all()
            serializer = SolicitudClienteNestedSerializer(solicitudes, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = SolicitudClienteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(servicio=servicio)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: en lugar de eliminar, marca el servicio como inactivo.
        """
        instance = self.get_object()
        instance.activo = False
        instance.save()
        return Response(
            {'message': 'Servicio desactivado correctamente'},
            status=status.HTTP_200_OK
        )


class SolicitudClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el modelo SolicitudCliente.
    
    Permite CRUD completo con filtros.
    """
    queryset = SolicitudCliente.objects.all()
    serializer_class = SolicitudClienteSerializer
    permission_classes = [AllowAny]  # En producción, usar permisos apropiados
    filter_backends = [DjangoFilterBackend]
    filterset_class = SolicitudClienteFilter

    def get_queryset(self):
        """
        Permite filtrado por servicio y estatus.
        """
        queryset = super().get_queryset()
        
        servicio_id = self.request.query_params.get('servicio', None)
        if servicio_id:
            queryset = queryset.filter(servicio_id=servicio_id)
        
        estatus = self.request.query_params.get('estatus', None)
        if estatus:
            queryset = queryset.filter(estatus=estatus)
        
        return queryset


