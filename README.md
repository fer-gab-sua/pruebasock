# Sistema de Gestión de Incidentes con Django y WebSockets

Sistema web para gestionar incidentes con actualización en tiempo real usando Django Channels y WebSockets.

## Características

- **Administración de Incidentes**: Crear y actualizar incidentes con su número y estado
- **Estados**: Pendiente, Asignada, Cerrada
- **Actualización en Tiempo Real**: La página de consulta se actualiza automáticamente usando WebSockets
- **Interfaz Moderna**: Diseño responsive y atractivo

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Crear y activar un entorno virtual (recomendado)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo de ejemplo y configura tus credenciales:

```powershell
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edita el archivo `.env` y completa con tus credenciales de Metabase:

```env
METABASE_URL=http://tu-servidor-metabase.com/
METABASE_USER=tu_usuario@ejemplo.com
METABASE_PASSWORD=tu_contraseña
METABASE_CARD_ID=51
```

**Nota**: El archivo `.env` está en `.gitignore` para no subir credenciales al repositorio.

### 4. Configurar la base de datos

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un superusuario (opcional, para acceder al admin de Django)

```powershell
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

## Ejecutar la Aplicación

```powershell
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## URLs Disponibles

- **Administración**: `http://127.0.0.1:8000/administracion/`
  - Crear nuevos incidentes
  - Actualizar estado de incidentes existentes
  - Eliminar incidentes

- **Consulta**: `http://127.0.0.1:8000/consulta/`
  - Ver todos los incidentes en tiempo real
  - Actualización automática cuando hay cambios
  - Estadísticas de incidentes por estado

- **Admin Django**: `http://127.0.0.1:8000/admin/`
  - Panel de administración de Django (requiere superusuario)

## Cómo Usar

### 1. Página de Administración

1. Accede a `/administracion/`
2. Ingresa un número de incidente (ej: INC-2024-001)
3. Selecciona el estado inicial
4. Haz clic en "Guardar Incidente"
5. El incidente aparecerá en la lista
6. Puedes cambiar el estado usando el selector
7. Puedes eliminar incidentes con el botón "Eliminar"

### 2. Página de Consulta

1. Accede a `/consulta/`
2. Verás todos los incidentes en tarjetas
3. El indicador en la parte superior mostrará si estás conectado
4. Cuando alguien actualice un incidente en la página de administración, verás los cambios automáticamente
5. Las estadísticas se actualizan en tiempo real

## Tecnologías Utilizadas

- **Django 4.2**: Framework web de Python
- **Django Channels**: Soporte para WebSockets y protocolos asíncronos
- **Daphne**: Servidor ASGI para Django Channels
- **SQLite**: Base de datos (incluida con Python)
- **WebSockets**: Para actualizaciones en tiempo real

## Estructura del Proyecto

```
pruebasock/
├── manage.py                          # Script de gestión de Django
├── requirements.txt                   # Dependencias del proyecto
├── db.sqlite3                        # Base de datos (se crea automáticamente)
├── incidentes_project/               # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                   # Configuración general
│   ├── urls.py                       # URLs principales
│   ├── asgi.py                       # Configuración ASGI con WebSockets
│   └── wsgi.py                       # Configuración WSGI
└── incidentes/                       # Aplicación de incidentes
    ├── __init__.py
    ├── models.py                     # Modelo de Incidente
    ├── views.py                      # Vistas de administración y consulta
    ├── urls.py                       # URLs de la aplicación
    ├── consumers.py                  # Consumer de WebSocket
    ├── routing.py                    # Routing de WebSocket
    ├── admin.py                      # Configuración del admin
    ├── apps.py                       # Configuración de la app
    └── templates/
        └── incidentes/
            ├── administracion.html   # Página de administración
            └── consulta.html         # Página de consulta en tiempo real
```

## Características de WebSocket

- **Conexión automática**: Al abrir la página de consulta, se establece conexión WebSocket
- **Reconexión automática**: Si se pierde la conexión, intenta reconectar cada 3 segundos
- **Indicador de estado**: Muestra si estás conectado o desconectado
- **Actualización sin recargar**: Los cambios se reflejan inmediatamente sin necesidad de recargar la página

## Solución de Problemas

### Error: "No module named 'channels'"
```powershell
pip install -r requirements.txt
```

### Error: "no such table: incidentes_incidente"
```powershell
python manage.py makemigrations
python manage.py migrate
```

### WebSocket no conecta
- Verifica que el servidor esté ejecutándose
- Revisa la consola del navegador (F12) para ver errores
- Asegúrate de estar usando la URL correcta

## Próximas Mejoras Sugeridas

- Autenticación de usuarios
- Historial de cambios de estado
- Filtros y búsqueda de incidentes
- Exportación a Excel/PDF
- Notificaciones push
- Asignación de incidentes a usuarios
- Comentarios en incidentes
- Archivos adjuntos

## Licencia

Proyecto libre para uso educativo y comercial.
