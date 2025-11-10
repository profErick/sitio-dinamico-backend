import django_filters
from django.db import models
from .models import Servicio, SolicitudCliente


class ServicioFilter(django_filters.FilterSet):
    """
    Filtros para el modelo Servicio.
    """
    categoria = django_filters.ChoiceFilter(choices=Servicio.CATEGORIA_CHOICES)
    activo = django_filters.BooleanFilter()
    min_precio = django_filters.NumberFilter(field_name='precio_mxn', lookup_expr='gte')
    max_precio = django_filters.NumberFilter(field_name='precio_mxn', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')
    ordenar_por = django_filters.CharFilter(method='filter_ordenar')

    class Meta:
        model = Servicio
        fields = ['categoria', 'activo', 'min_precio', 'max_precio']

    def filter_search(self, queryset, name, value):
        """
        Búsqueda por nombre o descripción.
        """
        if value:
            return queryset.filter(
                models.Q(nombre__icontains=value) |
                models.Q(descripcion__icontains=value)
            )
        return queryset

    def filter_ordenar(self, queryset, name, value):
        """
        Ordenación por precio o fecha de publicación.
        Valores permitidos: precio_asc, precio_desc, fecha_asc, fecha_desc
        """
        if value == 'precio_asc':
            return queryset.order_by('precio_mxn')
        elif value == 'precio_desc':
            return queryset.order_by('-precio_mxn')
        elif value == 'fecha_asc':
            return queryset.order_by('fecha_publicacion')
        elif value == 'fecha_desc':
            return queryset.order_by('-fecha_publicacion')
        return queryset


class SolicitudClienteFilter(django_filters.FilterSet):
    """
    Filtros para el modelo SolicitudCliente.
    """
    estatus = django_filters.ChoiceFilter(choices=SolicitudCliente.ESTATUS_CHOICES)
    servicio = django_filters.NumberFilter(field_name='servicio__id')

    class Meta:
        model = SolicitudCliente
        fields = ['estatus', 'servicio']


