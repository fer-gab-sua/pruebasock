# Guía de Despliegue en Render

## Configuración Completa para Render.com

Esta aplicación Django con WebSockets está lista para desplegarse en Render.

### Archivos de Configuración

Los siguientes archivos son necesarios para el despliegue:

1. **build.sh** - Script de construcción
2. **render.yaml** - Configuración de Render
3. **requirements.txt** - Dependencias de Python

### Pasos para Desplegar en Render

#### 1. Preparar el Repositorio

Asegúrate de que todos los archivos estén en tu repositorio Git:

```bash
git add .
git commit -m "Configuración para Render"
git push
```

#### 2. Crear Servicio en Render

1. Ve a [render.com](https://render.com) e inicia sesión
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub/GitLab
4. Configuración:
   - **Name**: `incidentes-websocket` (o el nombre que prefieras)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `daphne -b 0.0.0.0 -p $PORT incidentes_project.asgi:application`

#### 3. Variables de Entorno en Render

En la sección "Environment Variables" de Render, agrega:

| Key | Value | Nota |
|-----|-------|------|
| `PYTHON_VERSION` | `3.12.0` | Versión de Python |
| `SECRET_KEY` | (genera una clave segura) | Click en "Generate" |
| `DEBUG` | `False` | IMPORTANTE: debe ser False en producción |

**Generar SECRET_KEY segura:**
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### 4. Configurar el Dominio

Tu aplicación estará disponible en: `https://tu-app-name.onrender.com`

**IMPORTANTE**: Actualiza `CSRF_TRUSTED_ORIGINS` en `settings.py` con tu dominio real:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://tu-app-name.onrender.com',  # Cambia esto por tu dominio real
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]
```

#### 5. Hacer el Script Ejecutable (en Linux/Mac)

Si estás en Linux/Mac, haz el script ejecutable:

```bash
chmod +x build.sh
git add build.sh
git commit -m "Hacer build.sh ejecutable"
git push
```

### Verificación del Despliegue

1. **Build Logs**: Revisa los logs de construcción en Render
2. **Deploy Logs**: Verifica que Daphne inicie correctamente
3. **Acceso Web**: Visita `https://tu-app-name.onrender.com/administracion/`
4. **WebSocket**: Verifica que `/consulta/` se conecte correctamente

### Solución de Problemas Comunes

#### Error: "Forbidden (403) CSRF verification failed"

**Solución**: Asegúrate de que tu dominio esté en `CSRF_TRUSTED_ORIGINS` en settings.py

```python
CSRF_TRUSTED_ORIGINS = [
    'https://pruebasock.onrender.com',  # Tu dominio de Render
]
```

#### Error: "DisallowedHost"

**Solución**: Ya está configurado `ALLOWED_HOSTS = ['*']` pero para producción es mejor:

```python
ALLOWED_HOSTS = [
    'pruebasock.onrender.com',
    '127.0.0.1',
    'localhost',
]
```

#### WebSocket no conecta (wss://)

**Verificar**:
1. El navegador está usando `wss://` (WebSocket Secure) en producción
2. Render soporta WebSockets (sí, lo hace)
3. Revisa la consola del navegador (F12) para errores

#### Base de datos SQLite se resetea

**Problema**: Render es efímero, SQLite se pierde en cada deploy.

**Solución**: Para producción, usa PostgreSQL de Render:

1. En Render: "New +" → "PostgreSQL"
2. Copia la "Internal Database URL"
3. Agrega a requirements.txt: `psycopg2-binary>=2.9.0`
4. Agrega variable de entorno: `DATABASE_URL` con la URL de PostgreSQL
5. Actualiza settings.py:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

### Características de Render

✅ **HTTPS automático** - Certificados SSL gratis
✅ **WebSocket support** - WSS (WebSocket Secure)
✅ **Auto-deploy** - Deploy automático en cada push
✅ **Environment variables** - Gestión segura de secretos
✅ **Logs en tiempo real** - Ver logs de aplicación

### Plan Gratuito de Render

- **Web Service**: Gratis (con limitaciones)
- **Spin down**: Se apaga después de 15 min de inactividad
- **Spin up**: Tarda ~1 minuto en despertar
- **Horas**: 750 horas gratis/mes

### URLs de la Aplicación

Una vez desplegada:

- **Administración**: `https://tu-app-name.onrender.com/administracion/`
- **Consulta**: `https://tu-app-name.onrender.com/consulta/`
- **Admin Django**: `https://tu-app-name.onrender.com/admin/`

### Comandos Útiles

Crear superusuario en Render (desde Dashboard → Shell):

```bash
python manage.py createsuperuser
```

Ver logs en tiempo real:

```bash
# En el Dashboard de Render → Logs
```

### Configuración Adicional Recomendada

#### Para mejor rendimiento:

1. **Upgrade a Render Pro**: $7/mes por servicio
2. **PostgreSQL**: Base de datos persistente
3. **Redis**: Para Channel Layers (WebSocket más robusto)

#### Configurar Redis para Channel Layers:

```python
# requirements.txt
channels-redis>=4.0.0

# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```

### Monitoreo

Render proporciona:
- Métricas de CPU/Memoria
- Logs en tiempo real
- Alertas de salud
- Histórico de deploys

### Siguiente Paso

Después del primer despliegue exitoso:

1. ✅ Verificar que la web cargue
2. ✅ Crear un incidente en /administracion/
3. ✅ Abrir /consulta/ en otra ventana
4. ✅ Verificar que el WebSocket conecte (punto verde)
5. ✅ Cambiar el estado del incidente
6. ✅ Confirmar que se actualice en tiempo real

¡Tu aplicación está lista para producción! 🚀
