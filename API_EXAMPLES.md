# Ejemplos de Uso del API - Amigo Secreto

## Secret Santa

### 1. Listar eventos de un usuario
```bash
curl -X GET "http://localhost:8000/api/secret-santa/events/?user=firebase_uid_123"
```

Respuesta:
```json
[
  {
    "id": 1,
    "name": "Amigo Secreto Navidad 2025",
    "created_by": "firebase_uid_123",
    "participants": [
      {"id": 1, "name": "Juan", "email": "juan@example.com"},
      {"id": 2, "name": "María", "email": "maria@example.com"}
    ],
    "assignments": [],
    "is_drawn": false,
    "created_at": "2025-12-18T04:00:00Z"
  }
]
```

### 2. Crear un evento
```bash
curl -X POST "http://localhost:8000/api/secret-santa/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Amigo Secreto Oficina",
    "created_by": "firebase_uid_123",
    "participants": [
      {"name": "Juan", "email": "juan@example.com"},
      {"name": "María", "email": "maria@example.com"},
      {"name": "Pedro", "email": "pedro@example.com"},
      {"name": "Ana", "email": "ana@example.com"}
    ]
  }'
```

Respuesta:
```json
{
  "id": 2,
  "name": "Amigo Secreto Oficina",
  "created_by": "firebase_uid_123",
  "participants": [
    {"id": 3, "name": "Juan", "email": "juan@example.com"},
    {"id": 4, "name": "María", "email": "maria@example.com"},
    {"id": 5, "name": "Pedro", "email": "pedro@example.com"},
    {"id": 6, "name": "Ana", "email": "ana@example.com"}
  ],
  "assignments": [],
  "is_drawn": false,
  "created_at": "2025-12-18T04:30:00Z"
}
```

### 3. Realizar sorteo
```bash
curl -X POST "http://localhost:8000/api/secret-santa/events/2/draw/"
```

Respuesta:
```json
{
  "id": 2,
  "name": "Amigo Secreto Oficina",
  "created_by": "firebase_uid_123",
  "participants": [
    {"id": 3, "name": "Juan", "email": "juan@example.com"},
    {"id": 4, "name": "María", "email": "maria@example.com"},
    {"id": 5, "name": "Pedro", "email": "pedro@example.com"},
    {"id": 6, "name": "Ana", "email": "ana@example.com"}
  ],
  "assignments": [
    {"giver_id": 3, "receiver_id": 4},
    {"giver_id": 4, "receiver_id": 5},
    {"giver_id": 5, "receiver_id": 6},
    {"giver_id": 6, "receiver_id": 3}
  ],
  "is_drawn": true,
  "created_at": "2025-12-18T04:30:00Z"
}
```

### 4. Obtener detalles de un evento
```bash
curl -X GET "http://localhost:8000/api/secret-santa/events/2/"
```

## Wishlist

### 1. Obtener wishlist de un usuario
```bash
curl -X GET "http://localhost:8000/api/wishlist/wishlists/?user=firebase_uid_123"
```

Respuesta:
```json
[
  {
    "id": 1,
    "user": "firebase_uid_123",
    "items": [
      {
        "id": 1,
        "title": "Libro de cocina",
        "reference": "https://amazon.com/libro-cocina",
        "created_at": "2025-12-18T04:00:00Z"
      },
      {
        "id": 2,
        "title": "Auriculares Bluetooth",
        "reference": "https://amazon.com/auriculares",
        "created_at": "2025-12-18T04:00:00Z"
      }
    ],
    "created_at": "2025-12-18T04:00:00Z",
    "updated_at": "2025-12-18T04:00:00Z"
  }
]
```

### 2. Crear wishlist
```bash
curl -X POST "http://localhost:8000/api/wishlist/wishlists/" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "firebase_uid_456",
    "items": [
      {
        "title": "Libro de cocina",
        "reference": "https://amazon.com/libro-cocina"
      },
      {
        "title": "Auriculares Bluetooth",
        "reference": "https://amazon.com/auriculares"
      },
      {
        "title": "Mochila deportiva",
        "reference": "https://amazon.com/mochila"
      }
    ]
  }'
```

Respuesta:
```json
{
  "id": 2,
  "user": "firebase_uid_456",
  "items": [
    {
      "id": 3,
      "title": "Libro de cocina",
      "reference": "https://amazon.com/libro-cocina",
      "created_at": "2025-12-18T05:00:00Z"
    },
    {
      "id": 4,
      "title": "Auriculares Bluetooth",
      "reference": "https://amazon.com/auriculares",
      "created_at": "2025-12-18T05:00:00Z"
    },
    {
      "id": 5,
      "title": "Mochila deportiva",
      "reference": "https://amazon.com/mochila",
      "created_at": "2025-12-18T05:00:00Z"
    }
  ],
  "created_at": "2025-12-18T05:00:00Z",
  "updated_at": "2025-12-18T05:00:00Z"
}
```

### 3. Actualizar wishlist (mismo endpoint POST - hace upsert)
```bash
curl -X POST "http://localhost:8000/api/wishlist/wishlists/" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "firebase_uid_456",
    "items": [
      {
        "title": "Nueva laptop",
        "reference": "https://amazon.com/laptop"
      }
    ]
  }'
```

## Postman Collection

### Crear una colección en Postman:

1. **Crear variable de entorno**
   - `base_url`: `http://localhost:8000/api`
   - `user_id`: `firebase_uid_test`

2. **Importar requests**:

#### Secret Santa - List Events
- Method: `GET`
- URL: `{{base_url}}/secret-santa/events/?user={{user_id}}`

#### Secret Santa - Create Event
- Method: `POST`
- URL: `{{base_url}}/secret-santa/events/`
- Body (JSON):
```json
{
  "name": "Test Event",
  "created_by": "{{user_id}}",
  "participants": [
    {"name": "Person 1", "email": "person1@test.com"},
    {"name": "Person 2", "email": "person2@test.com"}
  ]
}
```

#### Secret Santa - Perform Draw
- Method: `POST`
- URL: `{{base_url}}/secret-santa/events/1/draw/`

#### Wishlist - Get
- Method: `GET`
- URL: `{{base_url}}/wishlist/wishlists/?user={{user_id}}`

#### Wishlist - Create/Update
- Method: `POST`
- URL: `{{base_url}}/wishlist/wishlists/`
- Body (JSON):
```json
{
  "user": "{{user_id}}",
  "items": [
    {"title": "Item 1", "reference": "https://example.com/item1"},
    {"title": "Item 2", "reference": "https://example.com/item2"}
  ]
}
```

## Errores Comunes

### Error 400: Sorteo ya realizado
```json
{
  "error": "El sorteo ya ha sido realizado"
}
```

### Error 400: Participantes insuficientes
```json
{
  "error": "Se necesitan al menos 2 participantes para realizar el sorteo"
}
```

### Error 404: Evento no encontrado
```json
{
  "detail": "Not found."
}
```

### Error 400: Campo requerido
```json
{
  "user": ["This field is required."]
}
```
