# Backend - Amigo Secreto API

Backend REST API para la aplicación de Amigo Secreto, construido con Django y Django REST Framework.

## Configuración

### Variables de Entorno

Copia el archivo `.env` y configura las siguientes variables:

```env
# Database (Supabase PostgreSQL)
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your_host.supabase.co
DB_PORT=5432

# Django
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:
```bash
python manage.py migrate
```

4. Ejecutar servidor:
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## API Endpoints

### Secret Santa

- `GET /api/secret-santa/events/` - Listar eventos (filtrar por user: `?user=firebase_uid`)
- `POST /api/secret-santa/events/` - Crear nuevo evento
- `GET /api/secret-santa/events/{id}/` - Obtener detalles de evento
- `POST /api/secret-santa/events/{id}/draw/` - Realizar sorteo

### Wishlist

- `GET /api/wishlist/wishlists/` - Listar wishlists (filtrar por user: `?user=firebase_uid`)
- `POST /api/wishlist/wishlists/` - Crear/actualizar wishlist
- `GET /api/wishlist/wishlists/{id}/` - Obtener detalles de wishlist

## Estructura de la Base de Datos

### Secret Santa
- `secret_santa_events`: Eventos de sorteo
- `participants`: Participantes de cada evento
- `assignments`: Asignaciones del sorteo

### Wishlist
- `wishlists`: Listas de deseos por usuario
- `wishlist_items`: Items de cada lista

## Notas

- La autenticación se maneja en el frontend con Firebase
- El backend usa el Firebase UID como identificador de usuario
- La base de datos está alojada en Supabase (PostgreSQL)
