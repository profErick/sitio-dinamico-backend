from django.test import TestCase
from django.core.exceptions import ValidationError
from services.models import Servicio, SolicitudCliente


class ServicioModelTest(TestCase):
    """Tests para el modelo Servicio"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.servicio_data = {
            'nombre': 'Desarrollo Web',
            'categoria': 'Web',
            'descripcion': 'Desarrollo de aplicaciones web modernas',
            'precio_mxn': 50000.00,
            'activo': True,
            'nivel_prioridad': 3,
            'responsable_email': 'dev@example.com',
            'tiempo_estimado_dias': 30,
        }

    def test_crear_servicio_valido(self):
        """Test: Crear un servicio válido"""
        servicio = Servicio.objects.create(**self.servicio_data)
        self.assertIsNotNone(servicio.id)
        self.assertEqual(servicio.nombre, 'Desarrollo Web')
        self.assertEqual(servicio.categoria, 'Web')
        self.assertEqual(float(servicio.precio_mxn), 50000.00)

    def test_servicio_precio_negativo_invalido(self):
        """Test: No se puede crear servicio con precio negativo"""
        self.servicio_data['precio_mxn'] = -100.00
        servicio = Servicio(**self.servicio_data)
        with self.assertRaises(ValidationError):
            servicio.full_clean()

    def test_servicio_nivel_prioridad_fuera_rango(self):
        """Test: No se puede crear servicio con nivel de prioridad fuera de rango"""
        self.servicio_data['nivel_prioridad'] = 6
        servicio = Servicio(**self.servicio_data)
        with self.assertRaises(ValidationError):
            servicio.full_clean()

    def test_servicio_tiempo_estimado_negativo(self):
        """Test: No se puede crear servicio con tiempo estimado negativo"""
        self.servicio_data['tiempo_estimado_dias'] = -5
        servicio = Servicio(**self.servicio_data)
        with self.assertRaises(ValidationError):
            servicio.full_clean()


class SolicitudClienteModelTest(TestCase):
    """Tests para el modelo SolicitudCliente"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            categoria='Web',
            descripcion='Descripción test',
            precio_mxn=10000.00,
            responsable_email='test@example.com',
        )
        self.solicitud_data = {
            'servicio': self.servicio,
            'cliente_nombre': 'Juan Pérez',
            'cliente_email': 'juan@example.com',
            'mensaje': 'Quiero contratar este servicio',
            'estatus': 'nuevo',
        }

    def test_crear_solicitud_valida(self):
        """Test: Crear una solicitud válida"""
        solicitud = SolicitudCliente.objects.create(**self.solicitud_data)
        self.assertIsNotNone(solicitud.id)
        self.assertEqual(solicitud.cliente_nombre, 'Juan Pérez')
        self.assertEqual(solicitud.estatus, 'nuevo')

    def test_solicitud_mensaje_vacio_invalido(self):
        """Test: No se puede crear solicitud con mensaje vacío"""
        self.solicitud_data['mensaje'] = ''
        solicitud = SolicitudCliente(**self.solicitud_data)
        with self.assertRaises(ValidationError):
            solicitud.full_clean()

    def test_solicitud_relacion_con_servicio(self):
        """Test: La solicitud está correctamente relacionada con el servicio"""
        solicitud = SolicitudCliente.objects.create(**self.solicitud_data)
        self.assertEqual(solicitud.servicio, self.servicio)
        self.assertIn(solicitud, self.servicio.solicitudes.all())


