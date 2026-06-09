# Aplicación Fullstack: Login + Bienvenida

Este repositorio contiene una solución fullstack con:

- **Backend** en FastAPI (`/backend`) con autenticación JWT.
- **Frontend** en React (`/frontend`) con página de login y página de bienvenida protegida.

El frontend sigue el estándar visual definido en `DESIGN.md` (paleta, tipografía Inter, ritmo de espaciado y estilo de superficies).

## Estructura del proyecto

```text
.
├── DESIGN.md
├── README.md
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── security.py
│   ├── requirements.txt
│   └── tests
│       └── test_auth.py
└── frontend
    ├── .env.example
    ├── package.json
    └── src
        ├── App.css
        ├── App.jsx
        ├── index.css
        └── main.jsx
```

## Backend (FastAPI)

### Requisitos

- Python 3.10+

### Instalación y ejecución

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Endpoints principales

- `POST /auth/login`
  - Body:
    ```json
    {
      "usuario": "admin",
      "password": "admin123"
    }
    ```
- `GET /api/me` (protegido por token Bearer)
- `GET /health`

## Frontend (React)

### Requisitos

- Node.js 20+

### Configuración

Crear archivo `.env` en `frontend` (o copiar `.env.example`):

```bash
cd frontend
cp .env.example .env
```

Variable disponible:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Instalación y ejecución

```bash
cd frontend
npm install
npm run dev
```

Aplicación disponible en `http://localhost:5173`.

## Flujo de autenticación

1. El usuario abre `/login`.
2. El formulario envía credenciales al backend (`POST /auth/login`).
3. Si son válidas, el frontend guarda `access_token` en **sessionStorage**.
4. El usuario es redirigido a `/welcome`.
5. La ruta `/welcome` está protegida y no permite acceso sin sesión.
6. En `/welcome` se consulta `/api/me` para mostrar el usuario autenticado.
7. Al cerrar sesión se elimina el token de `sessionStorage` y se vuelve a `/login`.

## Pruebas y validación

### Backend

```bash
cd backend
PYTHONPATH=. pytest -q
```

### Frontend

```bash
cd frontend
npm run lint
npm run build
```
