from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from services.models import Servicio, SolicitudCliente


class ServicioViewSetTest(TestCase):
    """Tests para ServicioViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        
        # Crear servicios de prueba
        self.servicio1 = Servicio.objects.create(
            nombre='Desarrollo Web',
            categoria='Web',
            descripcion='Desarrollo de aplicaciones web',
            precio_mxn=50000.00,
            responsable_email='web@example.com',
        )
        self.servicio2 = Servicio.objects.create(
            nombre='App Móvil',
            categoria='Móvil',
            descripcion='Desarrollo de aplicaciones móviles',
            precio_mxn=80000.00,
            responsable_email='mobile@example.com',
        )
        self.servicio3 = Servicio.objects.create(
            nombre='Cloud Service',
            categoria='Cloud',
            descripcion='Servicios en la nube',
            precio_mxn=30000.00,
            activo=False,
            responsable_email='cloud@example.com',
        )

    def test_listar_servicios(self):
        """Test: Listar todos los servicios"""
        url = reverse('servicio-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_crear_servicio_valido(self):
        """Test: Crear un servicio válido → 201"""
        url = reverse('servicio-list')
        data = {
            'nombre': 'Nuevo Servicio',
            'categoria': 'Data',
            'descripcion': 'Servicio de análisis de datos',
            'precio_mxn': '25000.00',
            'activo': True,
            'nivel_prioridad': 4,
            'responsable_email': 'data@example.com',
            'tiempo_estimado_dias': 15,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Servicio.objects.count(), 4)

    def test_crear_servicio_precio_negativo(self):
        """Test: Crear servicio con precio negativo → 400"""
        url = reverse('servicio-list')
        data = {
            'nombre': 'Servicio Inválido',
            'categoria': 'Web',
            'descripcion': 'Descripción',
            'precio_mxn': '-100.00',
            'responsable_email': 'test@example.com',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filtrar_por_categoria(self):
        """Test: Filtrar servicios por categoría"""
        url = reverse('servicio-list')
        response = self.client.get(url, {'categoria': 'Web'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['categoria'], 'Web')

    def test_filtrar_por_activo(self):
        """Test: Filtrar servicios activos"""
        url = reverse('servicio-list')
        response = self.client.get(url, {'activo': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filtrar_por_rango_precio(self):
        """Test: Filtrar servicios por rango de precio"""
        url = reverse('servicio-list')
        response = self.client.get(url, {'min_precio': '40000', 'max_precio': '60000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Desarrollo Web')

    def test_buscar_por_nombre(self):
        """Test: Búsqueda por nombre"""
        url = reverse('servicio-list')
        response = self.client.get(url, {'search': 'Web'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_ordenar_por_precio(self):
        """Test: Ordenar servicios por precio"""
        url = reverse('servicio-list')
        response = self.client.get(url, {'ordenar_por': 'precio_asc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        precios = [s['precio_mxn'] for s in response.data['results']]
        self.assertEqual(precios, sorted(precios))

    def test_obtener_servicio_por_id(self):
        """Test: Obtener un servicio específico"""
        url = reverse('servicio-detail', kwargs={'pk': self.servicio1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Desarrollo Web')

    def test_actualizar_servicio(self):
        """Test: Actualizar un servicio"""
        url = reverse('servicio-detail', kwargs={'pk': self.servicio1.id})
        data = {'nombre': 'Servicio Actualizado'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.servicio1.refresh_from_db()
        self.assertEqual(self.servicio1.nombre, 'Servicio Actualizado')

    def test_soft_delete_servicio(self):
        """Test: Soft delete de servicio (marcar como inactivo)"""
        url = reverse('servicio-detail', kwargs={'pk': self.servicio1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.servicio1.refresh_from_db()
        self.assertFalse(self.servicio1.activo)


class SolicitudClienteViewSetTest(TestCase):
    """Tests para SolicitudClienteViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            categoria='Web',
            descripcion='Descripción test',
            precio_mxn=10000.00,
            responsable_email='test@example.com',
        )

    def test_crear_solicitud_valida(self):
        """Test: Crear una solicitud válida"""
        url = reverse('solicitud-list')
        data = {
            'servicio': self.servicio.id,
            'cliente_nombre': 'Juan Pérez',
            'cliente_email': 'juan@example.com',
            'mensaje': 'Quiero contratar este servicio',
            'estatus': 'nuevo',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SolicitudCliente.objects.count(), 1)

    def test_crear_solicitud_email_invalido(self):
        """Test: Crear solicitud con email inválido → 400"""
        url = reverse('solicitud-list')
        data = {
            'servicio': self.servicio.id,
            'cliente_nombre': 'Juan Pérez',
            'cliente_email': 'email-invalido',
            'mensaje': 'Mensaje de prueba',
            'estatus': 'nuevo',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_solicitudes(self):
        """Test: Listar todas las solicitudes"""
        SolicitudCliente.objects.create(
            servicio=self.servicio,
            cliente_nombre='Cliente 1',
            cliente_email='cliente1@example.com',
            mensaje='Mensaje 1',
        )
        SolicitudCliente.objects.create(
            servicio=self.servicio,
            cliente_nombre='Cliente 2',
            cliente_email='cliente2@example.com',
            mensaje='Mensaje 2',
        )
        url = reverse('solicitud-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)


class SolicitudNestedTest(TestCase):
    """Tests para endpoints anidados de solicitudes"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = APIClient()
        self.servicio = Servicio.objects.create(
            nombre='Servicio Test',
            categoria='Web',
            descripcion='Descripción test',
            precio_mxn=10000.00,
            responsable_email='test@example.com',
        )

    def test_listar_solicitudes_de_servicio(self):
        """Test: Listar solicitudes de un servicio específico"""
        SolicitudCliente.objects.create(
            servicio=self.servicio,
            cliente_nombre='Cliente 1',
            cliente_email='cliente1@example.com',
            mensaje='Mensaje 1',
        )
        url = reverse('servicio-solicitudes', kwargs={'pk': self.servicio.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_solicitud_en_servicio(self):
        """Test: Crear solicitud anidada en un servicio"""
        url = reverse('servicio-solicitudes', kwargs={'pk': self.servicio.id})
        data = {
            'cliente_nombre': 'Cliente Nuevo',
            'cliente_email': 'nuevo@example.com',
            'mensaje': 'Nuevo mensaje',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.servicio.solicitudes.count(), 1)


