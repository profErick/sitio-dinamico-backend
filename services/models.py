from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.core.exceptions import ValidationError


class Servicio(models.Model):
    """
    Modelo para representar un servicio ofrecido.
    """
    CATEGORIA_CHOICES = [
        ('Web', 'Web'),
        ('Móvil', 'Móvil'),
        ('Cloud', 'Cloud'),
        ('Data', 'Data'),
        ('Seguridad', 'Seguridad'),
        ('Consultoría', 'Consultoría'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, help_text="Nombre del servicio")
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIA_CHOICES,
        help_text="Categoría del servicio"
    )
    descripcion = models.TextField(help_text="Descripción detallada del servicio")
    precio_mxn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Precio en pesos mexicanos"
    )
    activo = models.BooleanField(
        default=True,
        help_text="Indica si el servicio está activo"
    )
    nivel_prioridad = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nivel de prioridad del servicio (1-5)"
    )
    fecha_publicacion = models.DateField(
        auto_now_add=True,
        help_text="Fecha de publicación del servicio"
    )
    ultima_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de última actualización"
    )
    responsable_email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Email del responsable del servicio"
    )
    tiempo_estimado_dias = models.IntegerField(
        default=7,
        validators=[MinValueValidator(0)],
        help_text="Tiempo estimado de entrega en días"
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-fecha_publicacion', 'nombre']
        indexes = [
            models.Index(fields=['categoria', 'activo']),
            models.Index(fields=['precio_mxn']),
            models.Index(fields=['fecha_publicacion']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    def clean(self):
        """Validaciones adicionales del modelo"""
        if self.precio_mxn < 0:
            raise ValidationError({'precio_mxn': 'El precio no puede ser negativo'})
        if self.nivel_prioridad < 1 or self.nivel_prioridad > 5:
            raise ValidationError({'nivel_prioridad': 'El nivel de prioridad debe estar entre 1 y 5'})
        if self.tiempo_estimado_dias < 0:
            raise ValidationError({'tiempo_estimado_dias': 'El tiempo estimado no puede ser negativo'})


class SolicitudCliente(models.Model):
    """
    Modelo para representar una solicitud de cliente relacionada con un servicio.
    """
    ESTATUS_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado'),
    ]

    id = models.AutoField(primary_key=True)
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='solicitudes',
        help_text="Servicio relacionado"
    )
    cliente_nombre = models.CharField(
        max_length=120,
        help_text="Nombre del cliente"
    )
    cliente_email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Email del cliente"
    )
    mensaje = models.TextField(help_text="Mensaje de la solicitud")
    estatus = models.CharField(
        max_length=20,
        choices=ESTATUS_CHOICES,
        default='nuevo',
        help_text="Estatus de la solicitud"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación de la solicitud"
    )

    class Meta:
        verbose_name = "Solicitud de Cliente"
        verbose_name_plural = "Solicitudes de Clientes"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['servicio', 'estatus']),
            models.Index(fields=['fecha_creacion']),
        ]

    def __str__(self):
        return f"Solicitud de {self.cliente_nombre} - {self.servicio.nombre} ({self.estatus})"

    def clean(self):
        """Validaciones adicionales del modelo"""
        if not self.mensaje or not self.mensaje.strip():
            raise ValidationError({'mensaje': 'El mensaje no puede estar vacío'})


