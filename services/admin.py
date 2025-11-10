from django.contrib import admin
from .models import Servicio, SolicitudCliente


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_mxn', 'activo', 'nivel_prioridad', 'fecha_publicacion')
    list_filter = ('categoria', 'activo', 'nivel_prioridad', 'fecha_publicacion')
    search_fields = ('nombre', 'descripcion', 'responsable_email')
    readonly_fields = ('fecha_publicacion', 'ultima_actualizacion')
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'categoria', 'descripcion')
        }),
        ('Precio y Estado', {
            'fields': ('precio_mxn', 'activo', 'nivel_prioridad')
        }),
        ('Información Adicional', {
            'fields': ('responsable_email', 'tiempo_estimado_dias')
        }),
        ('Fechas', {
            'fields': ('fecha_publicacion', 'ultima_actualizacion')
        }),
    )


@admin.register(SolicitudCliente)
class SolicitudClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente_nombre', 'servicio', 'estatus', 'fecha_creacion')
    list_filter = ('estatus', 'fecha_creacion', 'servicio')
    search_fields = ('cliente_nombre', 'cliente_email', 'mensaje')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Cliente', {
            'fields': ('cliente_nombre', 'cliente_email')
        }),
        ('Solicitud', {
            'fields': ('servicio', 'mensaje', 'estatus')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',)
        }),
    )


