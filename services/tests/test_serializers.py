from django.test import TestCase
from rest_framework.exceptions import ValidationError
from services.models import Servicio, SolicitudCliente
from services.serializers import ServicioSerializer, SolicitudClienteSerializer


class ServicioSerializerTest(TestCase):
    """Tests para ServicioSerializer"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.valid_data = {
            'nombre': 'Desarrollo Web',
            'categoria': 'Web',
            'descripcion': 'Desarrollo de aplicaciones web modernas',
            'precio_mxn': '50000.00',
            'activo': True,
            'nivel_prioridad': 3,
            'responsable_email': 'dev@example.com',
            'tiempo_estimado_dias': 30,
        }

    def test_serializer_valido(self):
        """Test: Serializer con datos válidos"""
        serializer = ServicioSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_precio_negativo(self):
        """Test: Serializer rechaza precio negativo"""
        self.valid_data['precio_mxn'] = '-100.00'
        serializer = ServicioSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('precio_mxn', serializer.errors)

    def test_serializer_nivel_prioridad_fuera_rango(self):
        """Test: Serializer rechaza nivel de prioridad fuera de rango"""
        self.valid_data['nivel_prioridad'] = 6
        serializer = ServicioSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nivel_prioridad', serializer.errors)

    def test_serializer_email_invalido(self):
        """Test: Serializer rechaza email inválido"""
        self.valid_data['responsable_email'] = 'email-invalido'
        serializer = ServicioSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('responsable_email', serializer.errors)

    def test_serializer_nombre_vacio(self):
        """Test: Serializer rechaza nombre vacío"""
        self.valid_data['nombre'] = ''
        serializer = ServicioSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())


class SolicitudClienteSerializerTest(TestCase):
    """Tests para SolicitudClienteSerializer"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            categoria='Web',
            descripcion='Descripción test',
            precio_mxn=10000.00,
            responsable_email='test@example.com',
        )
        self.valid_data = {
            'servicio': self.servicio.id,
            'cliente_nombre': 'Juan Pérez',
            'cliente_email': 'juan@example.com',
            'mensaje': 'Quiero contratar este servicio',
            'estatus': 'nuevo',
        }

    def test_serializer_valido(self):
        """Test: Serializer con datos válidos"""
        serializer = SolicitudClienteSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_email_invalido(self):
        """Test: Serializer rechaza email inválido"""
        self.valid_data['cliente_email'] = 'email-invalido'
        serializer = SolicitudClienteSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cliente_email', serializer.errors)

    def test_serializer_mensaje_vacio(self):
        """Test: Serializer rechaza mensaje vacío"""
        self.valid_data['mensaje'] = ''
        serializer = SolicitudClienteSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('mensaje', serializer.errors)


