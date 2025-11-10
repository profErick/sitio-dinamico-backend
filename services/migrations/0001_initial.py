# Generated manually

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre del servicio', max_length=100)),
                ('categoria', models.CharField(choices=[('Web', 'Web'), ('Móvil', 'Móvil'), ('Cloud', 'Cloud'), ('Data', 'Data'), ('Seguridad', 'Seguridad'), ('Consultoría', 'Consultoría')], help_text='Categoría del servicio', max_length=50)),
                ('descripcion', models.TextField(help_text='Descripción detallada del servicio')),
                ('precio_mxn', models.DecimalField(decimal_places=2, help_text='Precio en pesos mexicanos', max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('activo', models.BooleanField(default=True, help_text='Indica si el servicio está activo')),
                ('nivel_prioridad', models.IntegerField(default=3, help_text='Nivel de prioridad del servicio (1-5)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('fecha_publicacion', models.DateField(auto_now_add=True, help_text='Fecha de publicación del servicio')),
                ('ultima_actualizacion', models.DateTimeField(auto_now=True, help_text='Fecha y hora de última actualización')),
                ('responsable_email', models.EmailField(help_text='Email del responsable del servicio', max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('tiempo_estimado_dias', models.IntegerField(default=7, help_text='Tiempo estimado de entrega en días', validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'ordering': ['-fecha_publicacion', 'nombre'],
            },
        ),
        migrations.AddIndex(
            model_name='servicio',
            index=models.Index(fields=['categoria', 'activo'], name='services_se_categor_idx'),
        ),
        migrations.AddIndex(
            model_name='servicio',
            index=models.Index(fields=['precio_mxn'], name='services_se_precio__idx'),
        ),
        migrations.AddIndex(
            model_name='servicio',
            index=models.Index(fields=['fecha_publicacion'], name='services_se_fecha_p_idx'),
        ),
        migrations.CreateModel(
            name='SolicitudCliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cliente_nombre', models.CharField(help_text='Nombre del cliente', max_length=120)),
                ('cliente_email', models.EmailField(help_text='Email del cliente', max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('mensaje', models.TextField(help_text='Mensaje de la solicitud')),
                ('estatus', models.CharField(choices=[('nuevo', 'Nuevo'), ('en_proceso', 'En Proceso'), ('cerrado', 'Cerrado')], default='nuevo', help_text='Estatus de la solicitud', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha y hora de creación de la solicitud')),
                ('servicio', models.ForeignKey(help_text='Servicio relacionado', on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='services.servicio')),
            ],
            options={
                'verbose_name': 'Solicitud de Cliente',
                'verbose_name_plural': 'Solicitudes de Clientes',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.AddIndex(
            model_name='solicitudcliente',
            index=models.Index(fields=['servicio', 'estatus'], name='services_so_servici_idx'),
        ),
        migrations.AddIndex(
            model_name='solicitudcliente',
            index=models.Index(fields=['fecha_creacion'], name='services_so_fecha_c_idx'),
        ),
    ]

