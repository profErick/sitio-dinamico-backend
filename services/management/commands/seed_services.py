from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from services.models import Servicio, SolicitudCliente


class Command(BaseCommand):
    help = 'Crea 10 servicios variados y 20 solicitudes de prueba'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando seed de datos...'))

        # Limpiar datos existentes (opcional, comentar si no se desea)
        # Servicio.objects.all().delete()
        # SolicitudCliente.objects.all().delete()

        # Crear 10 servicios variados
        servicios_data = [
            {
                'nombre': 'Desarrollo Web Full Stack',
                'categoria': 'Web',
                'descripcion': 'Desarrollo completo de aplicaciones web modernas con React y Django',
                'precio_mxn': 75000.00,
                'nivel_prioridad': 5,
                'responsable_email': 'web@empresa.com',
                'tiempo_estimado_dias': 60,
            },
            {
                'nombre': 'App Móvil iOS y Android',
                'categoria': 'Móvil',
                'descripcion': 'Desarrollo de aplicaciones móviles nativas para iOS y Android',
                'precio_mxn': 120000.00,
                'nivel_prioridad': 5,
                'responsable_email': 'mobile@empresa.com',
                'tiempo_estimado_dias': 90,
            },
            {
                'nombre': 'Migración a AWS',
                'categoria': 'Cloud',
                'descripcion': 'Migración completa de infraestructura a Amazon Web Services',
                'precio_mxn': 95000.00,
                'nivel_prioridad': 4,
                'responsable_email': 'cloud@empresa.com',
                'tiempo_estimado_dias': 45,
            },
            {
                'nombre': 'Análisis de Big Data',
                'categoria': 'Data',
                'descripcion': 'Análisis y procesamiento de grandes volúmenes de datos con Python y Spark',
                'precio_mxn': 85000.00,
                'nivel_prioridad': 4,
                'responsable_email': 'data@empresa.com',
                'tiempo_estimado_dias': 50,
            },
            {
                'nombre': 'Auditoría de Seguridad',
                'categoria': 'Seguridad',
                'descripcion': 'Auditoría completa de seguridad informática y recomendaciones',
                'precio_mxn': 65000.00,
                'nivel_prioridad': 5,
                'responsable_email': 'security@empresa.com',
                'tiempo_estimado_dias': 30,
            },
            {
                'nombre': 'Consultoría Estratégica IT',
                'categoria': 'Consultoría',
                'descripcion': 'Consultoría estratégica para transformación digital',
                'precio_mxn': 55000.00,
                'nivel_prioridad': 3,
                'responsable_email': 'consultoria@empresa.com',
                'tiempo_estimado_dias': 20,
            },
            {
                'nombre': 'E-commerce Platform',
                'categoria': 'Web',
                'descripcion': 'Plataforma completa de comercio electrónico con pasarela de pagos',
                'precio_mxn': 110000.00,
                'nivel_prioridad': 4,
                'responsable_email': 'ecommerce@empresa.com',
                'tiempo_estimado_dias': 75,
            },
            {
                'nombre': 'App React Native',
                'categoria': 'Móvil',
                'descripcion': 'Aplicación móvil multiplataforma desarrollada con React Native',
                'precio_mxn': 70000.00,
                'nivel_prioridad': 3,
                'responsable_email': 'react@empresa.com',
                'tiempo_estimado_dias': 55,
            },
            {
                'nombre': 'Data Warehouse en Azure',
                'categoria': 'Cloud',
                'descripcion': 'Implementación de almacén de datos en Microsoft Azure',
                'precio_mxn': 90000.00,
                'nivel_prioridad': 4,
                'responsable_email': 'azure@empresa.com',
                'tiempo_estimado_dias': 40,
            },
            {
                'nombre': 'Penetration Testing',
                'categoria': 'Seguridad',
                'descripcion': 'Pruebas de penetración y análisis de vulnerabilidades',
                'precio_mxn': 50000.00,
                'nivel_prioridad': 3,
                'responsable_email': 'pentest@empresa.com',
                'tiempo_estimado_dias': 25,
            },
        ]

        servicios_creados = []
        for data in servicios_data:
            servicio = Servicio.objects.create(**data)
            servicios_creados.append(servicio)
            self.stdout.write(
                self.style.SUCCESS(f'✓ Servicio creado: {servicio.nombre}')
            )

        # Crear 20 solicitudes distribuidas entre los servicios
        nombres_clientes = [
            'Juan Pérez', 'María González', 'Carlos Rodríguez', 'Ana Martínez',
            'Luis Hernández', 'Laura Sánchez', 'Roberto López', 'Patricia García',
            'Fernando Ramírez', 'Sofía Torres', 'Miguel Díaz', 'Carmen Flores',
            'Jorge Morales', 'Isabel Ruiz', 'Ricardo Vargas', 'Elena Castro',
            'Daniel Jiménez', 'Adriana Mendoza', 'Alejandro Ortega', 'Lucía Ríos',
        ]

        emails_clientes = [
            'juan.perez@email.com', 'maria.gonzalez@email.com', 'carlos.rodriguez@email.com',
            'ana.martinez@email.com', 'luis.hernandez@email.com', 'laura.sanchez@email.com',
            'roberto.lopez@email.com', 'patricia.garcia@email.com', 'fernando.ramirez@email.com',
            'sofia.torres@email.com', 'miguel.diaz@email.com', 'carmen.flores@email.com',
            'jorge.morales@email.com', 'isabel.ruiz@email.com', 'ricardo.vargas@email.com',
            'elena.castro@email.com', 'daniel.jimenez@email.com', 'adriana.mendoza@email.com',
            'alejandro.ortega@email.com', 'lucia.rios@email.com',
        ]

        mensajes = [
            'Me interesa contratar este servicio para mi empresa',
            'Necesito más información sobre los detalles y el proceso',
            '¿Cuál es el tiempo de entrega estimado?',
            'Quiero agendar una reunión para discutir el proyecto',
            'Estoy interesado en conocer los precios y paquetes disponibles',
            'Necesito una solución urgente para mi negocio',
            'Me gustaría recibir una propuesta personalizada',
            '¿Ofrecen soporte post-implementación?',
            'Tengo un proyecto grande y necesito cotización',
            'Busco una solución escalable y moderna',
            'Necesito integrar esto con mis sistemas existentes',
            '¿Pueden trabajar con mi equipo interno?',
            'Quiero saber más sobre la metodología de trabajo',
            'Necesito una demo o prueba del servicio',
            'Estoy evaluando varias opciones, ¿qué me recomiendan?',
            'Tengo un presupuesto limitado, ¿hay opciones flexibles?',
            'Necesito implementación rápida, ¿es posible?',
            'Quiero conocer casos de éxito similares',
            '¿Ofrecen capacitación para mi equipo?',
            'Necesito una solución personalizada para mi industria',
        ]

        estatus_opciones = ['nuevo', 'en_proceso', 'cerrado']

        for i in range(20):
            servicio = random.choice(servicios_creados)
            estatus = random.choice(estatus_opciones)
            
            # Crear fecha de creación variada (últimos 30 días)
            fecha_creacion = timezone.now() - timedelta(days=random.randint(0, 30))
            
            solicitud = SolicitudCliente.objects.create(
                servicio=servicio,
                cliente_nombre=nombres_clientes[i],
                cliente_email=emails_clientes[i],
                mensaje=mensajes[i],
                estatus=estatus,
            )
            # Actualizar fecha_creacion manualmente
            SolicitudCliente.objects.filter(id=solicitud.id).update(fecha_creacion=fecha_creacion)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Solicitud creada: {solicitud.cliente_nombre} - {servicio.nombre}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Seed completado: {len(servicios_creados)} servicios y 20 solicitudes creadas'
            )
        )


