# FastAPI JWT Authentication Backend

Aplicación Web API desarrollada con **FastAPI** y **Python** que implementa autenticación con **JWT (JSON Web Tokens)**.

## Descripción

Esta es una aplicación backend que proporciona autenticación basada en tokens JWT. Incluye endpoints para:
- **Login**: Autentica al usuario y retorna un token de acceso con expiración de 300 segundos
- **Refresh Token**: Refresca el token de acceso usando un token de actualización
- **Obtener Usuario Actual**: Endpoint protegido que devuelve la información del usuario autenticado

## Características

- ✅ Autenticación basada en JWT
- ✅ Token de acceso con expiración de 300 segundos (5 minutos)
- ✅ Token de refresco con expiración de 7 días
- ✅ Endpoint protegido con validación de token
- ✅ CORS habilitado
- ✅ Documentación automática con Swagger UI
- ✅ Gestión de dependencias con Poetry
- ✅ Dockerfile y docker-compose.yml incluidos
- ✅ Health checks implementados

## Requisitos Previos

- Python 3.10 o superior
- Poetry (gestor de dependencias de Python)
- Docker y Docker Compose (opcional, para ejecutar en contenedores)

## Instalación Local

### 1. Clonar o descargar el proyecto
```bash
cd backend
```

### 2. Instalar dependencias con Poetry
```bash
poetry install
```

### 3. Activar el entorno virtual
```bash
poetry shell
```

### 4. Ejecutar la aplicación
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

La aplicación estará disponible en `http://localhost:8000`

## Ejecución con Docker

### 1. Construir la imagen Docker
```bash
docker-compose build
```

### 2. Ejecutar el contenedor
```bash
docker-compose up -d
```

### 3. Verificar que está corriendo
```bash
docker-compose ps
docker logs fastapi-jwt-backend
```

### 4. Detener el contenedor
```bash
docker-compose down
```

## Credenciales Predeterminadas

- **Usuario**: `admin`
- **Contraseña**: `admin123`

## Endpoints API

### 1. Health Check
```
GET /health
```
Respuesta:
```json
{
  "status": "healthy"
}
```

### 2. Login - Obtener Token de Acceso
```
POST /auth/login
```

**Body (JSON):**
```json
{
  "usuario": "admin",
  "password": "admin123"
}
```

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 3. Refresh Token - Obtener Nuevo Token de Acceso
```
POST /auth/refresh
```

**Body (JSON):**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Respuesta (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 300
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired refresh token"
}
```

### 4. Obtener Usuario Actual (Endpoint Protegido)
```
GET /api/me
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Respuesta (200 OK):**
```json
{
  "usuario": "admin",
  "id": null
}
```

**Error (401 Unauthorized):**
```json
{
  "detail": "Invalid or expired token"
}
```

## Documentación Interactiva

La aplicación incluye documentación interactiva automática:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuración

Las variables de entorno se pueden configurar en un archivo `.env`:

```env
SECRET_KEY=your-super-secret-key-change-in-production
PYTHONUNBUFFERED=1
```

Para desarrollo, copiar el archivo `.env.example` a `.env`:
```bash
cp .env.example .env
```

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py          # Inicializador del módulo
│   ├── main.py              # Aplicación FastAPI principal
│   ├── models.py            # Modelos Pydantic
│   └── security.py          # Utilidades de seguridad JWT
├── pyproject.toml           # Configuración de Poetry
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Configuración Docker Compose
├── .dockerignore             # Archivos a ignorar en Docker
├── .env.example             # Ejemplo de variables de entorno
└── README.md                # Este archivo
```

## Dependencias Principales

- **FastAPI**: Framework web moderno y rápido
- **Uvicorn**: Servidor ASGI para ejecutar FastAPI
- **Pydantic**: Validación de datos y serialización
- **PyJWT**: Creación y validación de JSON Web Tokens
- **python-dotenv**: Gestión de variables de entorno

## Flujo de Autenticación

```
1. Usuario envía credenciales al endpoint /auth/login
   └─> {usuario: "admin", password: "admin123"}
   
2. Servidor valida credenciales
   └─> Si son válidas, genera un JWT access token
   
3. Cliente recibe el token con expiración de 300 segundos
   └─> {access_token: "...", token_type: "bearer", expires_in: 300}
   
4. Cliente usa el token en headers para acceder a endpoints protegidos
   └─> Authorization: Bearer <access_token>
   
5. Cuando el token expira, cliente lo refresca usando /auth/refresh
   └─> {refresh_token: "..."}
   
6. Servidor retorna un nuevo access token
   └─> {access_token: "...", token_type: "bearer", expires_in: 300}
```

## Testing

Para ejecutar los tests (si los hay):

```bash
poetry run pytest
```

## Producción

Para desplegar en producción:

1. **Cambiar la SECRET_KEY** en variables de entorno a algo más seguro
2. **Configurar un certificado SSL/TLS** (usar nginx o similar como proxy)
3. **Usar una base de datos real** en lugar de credenciales hardcodeadas
4. **Implementar rate limiting** para proteger contra ataques
5. **Habilitar logging y monitoreo**
6. **Usar un secreto fuerte para JWT**

## Ejemplos de Uso con curl

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"usuario":"admin","password":"admin123"}'
```

### Obtener usuario actual
```bash
curl -X GET "http://localhost:8000/api/me" \
  -H "Authorization: Bearer <access_token>"
```

## Solución de Problemas

### El contenedor no inicia
```bash
docker logs fastapi-jwt-backend
```

### Port 8000 ya está en uso
```bash
# Cambiar puerto en docker-compose.yml
# O liberar el puerto:
lsof -i :8000
kill -9 <PID>
```

### Token expirado
Esperar a que expire (300 segundos) o usar el endpoint de refresh para obtener uno nuevo.

## Licencia

MIT

## Contacto

Para preguntas o soporte, contactar al equipo de desarrollo.
