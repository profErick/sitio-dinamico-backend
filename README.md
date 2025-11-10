# Backend Django - API REST para Servicios

Backend desarrollado con Django 5.0 y Django REST Framework para gestionar servicios y solicitudes de clientes.

## 🚀 Características

- **CRUD completo** para Servicios y Solicitudes de Clientes
- **Filtros avanzados**: por categoría, precio, estado, búsqueda por texto
- **Ordenación**: por precio, fecha de publicación
- **Paginación**: 20 resultados por página
- **Validaciones robustas** en modelos y serializers
- **Manejo de errores** con respuestas JSON consistentes
- **CORS habilitado** para frontend en Netlify
- **Soporte multi-BD**: SQLite en desarrollo, PostgreSQL en producción
- **Tests completos** para modelos, serializers y vistas
- **Comando de seed** para datos de prueba

## 📋 Requisitos

- Python 3.10 o superior
- pip
- PostgreSQL (opcional, solo para producción)

## 🔧 Instalación

### 1. Clonar el repositorio y navegar al directorio

```bash
cd backend
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env` y configura las variables:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://tu-sitio.netlify.app
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario (opcional, para admin)

```bash
python manage.py createsuperuser
```

### 7. Cargar datos de prueba (opcional)

```bash
python manage.py seed_services
```

Este comando crea:
- 10 servicios variados
- 20 solicitudes de clientes distribuidas

### 8. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Endpoints de la API

### Health Check

```
GET /api/health
```

Respuesta:
```json
{
  "status": "ok"
}
```

### Servicios

#### Listar servicios
```
GET /api/servicios/
```

**Parámetros de consulta:**
- `categoria`: Filtrar por categoría (Web, Móvil, Cloud, Data, Seguridad, Consultoría)
- `activo`: Filtrar por estado activo (true/false)
- `min_precio`: Precio mínimo
- `max_precio`: Precio máximo
- `search`: Búsqueda por nombre o descripción
- `ordenar_por`: Ordenar por `precio_asc`, `precio_desc`, `fecha_asc`, `fecha_desc`
- `page`: Número de página (paginación)

**Ejemplo:**
```
GET /api/servicios/?categoria=Web&min_precio=50000&ordenar_por=precio_asc
```

#### Crear servicio
```
POST /api/servicios/
```

**Body (JSON):**
```json
{
  "nombre": "Desarrollo Web",
  "categoria": "Web",
  "descripcion": "Desarrollo de aplicaciones web modernas",
  "precio_mxn": "50000.00",
  "activo": true,
  "nivel_prioridad": 3,
  "responsable_email": "dev@example.com",
  "tiempo_estimado_dias": 30
}
```

#### Obtener servicio por ID
```
GET /api/servicios/{id}/
```

#### Actualizar servicio (completo)
```
PUT /api/servicios/{id}/
```

#### Actualizar servicio (parcial)
```
PATCH /api/servicios/{id}/
```

#### Eliminar servicio (soft delete)
```
DELETE /api/servicios/{id}/
```

Marca el servicio como inactivo en lugar de eliminarlo.

#### Listar solicitudes de un servicio
```
GET /api/servicios/{id}/solicitudes/
```

#### Crear solicitud para un servicio
```
POST /api/servicios/{id}/solicitudes/
```

**Body (JSON):**
```json
{
  "cliente_nombre": "Juan Pérez",
  "cliente_email": "juan@example.com",
  "mensaje": "Quiero contratar este servicio",
  "estatus": "nuevo"
}
```

### Solicitudes

#### Listar todas las solicitudes
```
GET /api/solicitudes/
```

**Parámetros de consulta:**
- `servicio`: Filtrar por ID de servicio
- `estatus`: Filtrar por estatus (nuevo, en_proceso, cerrado)

#### Crear solicitud
```
POST /api/solicitudes/
```

**Body (JSON):**
```json
{
  "servicio": 1,
  "cliente_nombre": "Juan Pérez",
  "cliente_email": "juan@example.com",
  "mensaje": "Mensaje de la solicitud",
  "estatus": "nuevo"
}
```

#### Obtener solicitud por ID
```
GET /api/solicitudes/{id}/
```

#### Actualizar solicitud
```
PUT /api/solicitudes/{id}/
PATCH /api/solicitudes/{id}/
```

#### Eliminar solicitud
```
DELETE /api/solicitudes/{id}/
```

## 🗄️ Modelos

### Servicio

- `id`: AutoField (PK)
- `nombre`: CharField (max 100, requerido)
- `categoria`: CharField (choices: Web, Móvil, Cloud, Data, Seguridad, Consultoría)
- `descripcion`: TextField (requerido)
- `precio_mxn`: DecimalField (max_digits=10, decimal_places=2, >= 0)
- `activo`: BooleanField (default=True)
- `nivel_prioridad`: IntegerField (default=3, rango 1-5)
- `fecha_publicacion`: DateField (auto_now_add)
- `ultima_actualizacion`: DateTimeField (auto_now)
- `responsable_email`: EmailField (requerido)
- `tiempo_estimado_dias`: IntegerField (default=7, >= 0)

### SolicitudCliente

- `id`: AutoField (PK)
- `servicio`: ForeignKey a Servicio (CASCADE)
- `cliente_nombre`: CharField (max 120, requerido)
- `cliente_email`: EmailField (requerido)
- `mensaje`: TextField (requerido, no vacío)
- `estatus`: CharField (choices: nuevo, en_proceso, cerrado, default=nuevo)
- `fecha_creacion`: DateTimeField (auto_now_add)

## ✅ Validaciones

### Servicio
- Precio no puede ser negativo
- Nivel de prioridad debe estar entre 1 y 5
- Email del responsable debe ser válido
- Tiempo estimado no puede ser negativo
- Nombre y descripción no pueden estar vacíos

### SolicitudCliente
- Email del cliente debe ser válido
- Mensaje no puede estar vacío
- Nombre del cliente no puede estar vacío

## 🧪 Tests

Ejecutar todos los tests:

```bash
python manage.py test
```

Ejecutar tests específicos:

```bash
python manage.py test services.tests.test_models
python manage.py test services.tests.test_serializers
python manage.py test services.tests.test_views
```

## 🚢 Despliegue en Producción

### Variables de Entorno Requeridas

Configura estas variables en tu plataforma de despliegue:

```env
SECRET_KEY=tu-secret-key-seguro-generado-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=tu-backend.onrender.com,tu-backend.railway.app
CORS_ALLOWED_ORIGINS=https://tu-sitio.netlify.app
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

**Nota importante:**
- Genera un `SECRET_KEY` seguro (puedes usar: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG` debe ser `False` en producción
- `ALLOWED_HOSTS` debe incluir el dominio de tu backend desplegado
- `CORS_ALLOWED_ORIGINS` debe apuntar a la URL de tu frontend en Netlify

### Despliegue en Render

#### 1. Preparar el Repositorio

Asegúrate de tener el archivo `Procfile` en la raíz del backend:
```
web: python manage.py migrate && gunicorn core.wsgi --bind 0.0.0.0:$PORT
```

#### 2. Crear Servicio en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub/GitLab
4. Selecciona el repositorio y la rama

#### 3. Configuración del Servicio

**Configuración básica:**
- **Name**: `sitio-dinamico-backend` (o el nombre que prefieras)
- **Region**: Elige la región más cercana
- **Branch**: `main` o `master`
- **Root Directory**: `backend` (si el backend está en una subcarpeta)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: *(dejar vacío, Render usará el Procfile)*

#### 4. Configurar Base de Datos PostgreSQL

1. En Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configura la base de datos:
   - **Name**: `sitio-dinamico-db`
   - **Database**: `sitio_dinamico`
   - **User**: Se genera automáticamente
   - **Region**: Misma región que el servicio web
3. Guarda la **Internal Database URL** que se genera

#### 5. Variables de Entorno

En la configuración del Web Service, ve a **"Environment"** y agrega:

```
SECRET_KEY=tu-secret-key-generado-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=tu-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://tu-sitio.netlify.app
DATABASE_URL=<Internal Database URL de PostgreSQL>
```

**Opcional - Variables individuales de PostgreSQL:**
Si prefieres usar variables individuales en lugar de `DATABASE_URL`:
```
POSTGRES_DB=sitio_dinamico
POSTGRES_USER=<usuario-generado>
POSTGRES_PASSWORD=<contraseña-generada>
POSTGRES_HOST=<host-interno>
POSTGRES_PORT=5432
```

#### 6. Desplegar

1. Click en **"Create Web Service"**
2. Render ejecutará automáticamente:
   - `pip install -r requirements.txt`
   - `python manage.py migrate` (desde el Procfile)
   - `gunicorn core.wsgi --bind 0.0.0.0:$PORT`
3. Espera a que el despliegue termine (5-10 minutos)

#### 7. Verificar Despliegue

Una vez desplegado, tu API estará disponible en:
```
https://tu-backend.onrender.com
```

**Endpoint público de verificación:**
```
GET https://tu-backend.onrender.com/api/health
```

Debería responder:
```json
{
  "status": "ok"
}
```

### Despliegue en Railway

#### 1. Preparar el Repositorio

El archivo `Procfile` es opcional en Railway, pero recomendado:
```
web: python manage.py migrate && gunicorn core.wsgi --bind 0.0.0.0:$PORT
```

#### 2. Crear Proyecto en Railway

1. Ve a [Railway Dashboard](https://railway.app/)
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Conecta tu repositorio y selecciona la rama

#### 3. Agregar Base de Datos PostgreSQL

1. En el proyecto, click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway creará automáticamente una base de datos PostgreSQL
3. La variable `DATABASE_URL` se configurará automáticamente

#### 4. Configurar Variables de Entorno

En la configuración del servicio, ve a **"Variables"** y agrega:

```
SECRET_KEY=tu-secret-key-generado-aleatoriamente
DEBUG=False
ALLOWED_HOSTS=tu-backend.railway.app
CORS_ALLOWED_ORIGINS=https://tu-sitio.netlify.app
```

**Nota:** `DATABASE_URL` se configura automáticamente cuando agregas PostgreSQL.

#### 5. Configurar el Servicio

1. Click en el servicio web
2. Ve a **"Settings"**
3. **Root Directory**: `backend` (si el backend está en una subcarpeta)
4. **Start Command**: *(dejar vacío si usas Procfile, o usar: `python manage.py migrate && gunicorn core.wsgi`)*

#### 6. Desplegar

1. Railway detectará automáticamente Django
2. Ejecutará las migraciones desde el Procfile
3. Iniciará Gunicorn
4. Tu API estará disponible en el dominio generado por Railway

#### 7. Verificar Despliegue

**Endpoint público:**
```
GET https://tu-backend.railway.app/api/health
```

### Migraciones Automáticas

Las migraciones se ejecutan automáticamente al arrancar gracias al `Procfile`:
```
web: python manage.py migrate && gunicorn core.wsgi --bind 0.0.0.0:$PORT
```

**Alternativa (si no usas Procfile):**
Puedes configurar un script de inicio en el panel de Render/Railway:
```bash
python manage.py migrate && gunicorn core.wsgi --bind 0.0.0.0:$PORT
```

### Cargar Datos de Prueba en Producción

Después del despliegue, puedes ejecutar el comando de seed desde la consola de Render/Railway:

```bash
python manage.py seed_services
```

O conectarte por SSH y ejecutarlo manualmente.

### Endpoint Público Documentado

Una vez desplegado, tu API estará disponible públicamente en:

**Base URL:**
```
https://tu-backend.onrender.com/api
```
o
```
https://tu-backend.railway.app/api
```

**Endpoints principales:**
- `GET /api/health` - Health check
- `GET /api/servicios/` - Listar servicios
- `POST /api/servicios/` - Crear servicio
- `GET /api/servicios/{id}/` - Obtener servicio
- `GET /api/servicios/{id}/solicitudes/` - Listar solicitudes de un servicio
- `POST /api/servicios/{id}/solicitudes/` - Crear solicitud

### Verificación Post-Despliegue

#### 1. Health Check
```bash
curl https://tu-backend.onrender.com/api/health
```
**Respuesta esperada:**
```json
{"status":"ok"}
```

#### 2. Verificar Tests
Ejecuta los tests antes de desplegar:
```bash
python manage.py test
```
Todos los tests deben pasar.

#### 3. Verificar Base de Datos
- Conecta a PostgreSQL desde Render/Railway
- Verifica que las tablas `services_servicio` y `services_solicitudcliente` existen
- Ejecuta `python manage.py seed_services` para cargar datos de prueba
- Verifica que los datos se crearon correctamente

#### 4. Probar Endpoints con Postman/curl

**Listar servicios:**
```bash
curl https://tu-backend.onrender.com/api/servicios/
```

**Crear servicio:**
```bash
curl -X POST https://tu-backend.onrender.com/api/servicios/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Servicio Test",
    "categoria": "Web",
    "descripcion": "Descripción de prueba",
    "precio_mxn": "50000.00",
    "responsable_email": "test@example.com"
  }'
```

### Troubleshooting

**Error: "DisallowedHost"**
- Verifica que `ALLOWED_HOSTS` incluye el dominio de tu backend

**Error: "Database connection failed"**
- Verifica que `DATABASE_URL` está configurado correctamente
- Asegúrate de que PostgreSQL está corriendo

**Error: "CORS blocked"**
- Verifica que `CORS_ALLOWED_ORIGINS` incluye la URL de tu frontend

**Migraciones no se ejecutan:**
- Verifica que el `Procfile` está en la raíz del backend
- Revisa los logs de Render/Railway para ver errores

## 📝 Comandos útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ejecutar servidor
python manage.py runserver

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba
python manage.py seed_services

# Ejecutar tests
python manage.py test

# Acceder al admin
# http://localhost:8000/admin
```

## 🔒 Seguridad

- **CSRF**: Configurado con `CSRF_TRUSTED_ORIGINS`
- **CORS**: Configurado para dominios específicos
- **Validación**: Datos sanitizados y validados
- **Errores**: Respuestas JSON consistentes sin exponer información sensible

## 📄 Estructura del proyecto

```
backend/
├── core/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── exceptions.py
├── services/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   └── commands/
│   │       └── seed_services.py
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_serializers.py
│       └── test_views.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

