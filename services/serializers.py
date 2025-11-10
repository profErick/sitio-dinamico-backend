from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import Servicio, SolicitudCliente


class ServicioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Servicio con validaciones personalizadas.
    """
    class Meta:
        model = Servicio
        fields = [
            'id',
            'nombre',
            'categoria',
            'descripcion',
            'precio_mxn',
            'activo',
            'nivel_prioridad',
            'fecha_publicacion',
            'ultima_actualizacion',
            'responsable_email',
            'tiempo_estimado_dias',
        ]
        read_only_fields = ['id', 'fecha_publicacion', 'ultima_actualizacion']

    def validate_precio_mxn(self, value):
        """Valida que el precio sea mayor o igual a 0"""
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value

    def validate_nivel_prioridad(self, value):
        """Valida que el nivel de prioridad esté entre 1 y 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("El nivel de prioridad debe estar entre 1 y 5.")
        return value

    def validate_responsable_email(self, value):
        """Valida que el email sea válido"""
        validator = EmailValidator()
        try:
            validator(value)
        except Exception:
            raise serializers.ValidationError("El email proporcionado no es válido.")
        return value

    def validate_tiempo_estimado_dias(self, value):
        """Valida que el tiempo estimado sea mayor o igual a 0"""
        if value < 0:
            raise serializers.ValidationError("El tiempo estimado no puede ser negativo.")
        return value

    def validate(self, data):
        """Validaciones adicionales a nivel de objeto"""
        # Validar que nombre no esté vacío
        if 'nombre' in data and (not data['nombre'] or not data['nombre'].strip()):
            raise serializers.ValidationError({'nombre': 'El nombre no puede estar vacío.'})
        
        # Validar que descripcion no esté vacía
        if 'descripcion' in data and (not data['descripcion'] or not data['descripcion'].strip()):
            raise serializers.ValidationError({'descripcion': 'La descripción no puede estar vacía.'})
        
        return data


class SolicitudClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SolicitudCliente con validaciones personalizadas.
    """
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    
    class Meta:
        model = SolicitudCliente
        fields = [
            'id',
            'servicio',
            'servicio_nombre',
            'cliente_nombre',
            'cliente_email',
            'mensaje',
            'estatus',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'fecha_creacion']

    def validate_cliente_email(self, value):
        """Valida que el email sea válido"""
        validator = EmailValidator()
        try:
            validator(value)
        except Exception:
            raise serializers.ValidationError("El email proporcionado no es válido.")
        return value

    def validate_mensaje(self, value):
        """Valida que el mensaje no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El mensaje no puede estar vacío.")
        return value

    def validate_cliente_nombre(self, value):
        """Valida que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del cliente no puede estar vacío.")
        return value

    def validate(self, data):
        """Validaciones adicionales a nivel de objeto"""
        # Validar que mensaje no esté vacío
        if 'mensaje' in data and (not data['mensaje'] or not data['mensaje'].strip()):
            raise serializers.ValidationError({'mensaje': 'El mensaje no puede estar vacío.'})
        
        return data


class SolicitudClienteNestedSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para solicitudes anidadas en servicios.
    """
    class Meta:
        model = SolicitudCliente
        fields = [
            'id',
            'cliente_nombre',
            'cliente_email',
            'mensaje',
            'estatus',
            'fecha_creacion',
        ]
        read_only_fields = ['id', 'fecha_creacion']


