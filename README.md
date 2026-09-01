#  Mail System API — FastAPI + Vue + PostgreSQL

Sistema de correo web desarrollado con una arquitectura **Frontend + Backend desacoplada**, implementando autenticación mediante **JWT**, gestión de usuarios y un sistema de mensajería con bandejas de entrada, enviados y papelera.

> Proyecto académico orientado al aprendizaje de arquitecturas REST, autenticación segura y desarrollo Full Stack.

---

##  Tecnologías

### Backend

- **FastAPI**
- **Python 3.10**
- **SQLAlchemy ORM**
- **PostgreSQL**
- **JWT (JSON Web Token)**
- **Passlib + bcrypt**
- **Uvicorn**

### Frontend

- **Vue 3**
- **Pinia**
- **Vue Router**
- **Axios**
- **Vite**

---

##  Arquitectura

```text
Frontend (Vue 3)
        │
        │ Axios
        ▼
FastAPI REST API
        │
        │ SQLAlchemy
        ▼
 PostgreSQL
```

El frontend consume la API mediante Axios y la autenticación se realiza utilizando **Bearer Tokens (JWT)**.

---

##  Funcionalidades implementadas

### Autenticación

- Registro de usuarios
- Inicio de sesión
- Contraseñas cifradas con bcrypt
- Generación de JWT
- Rutas protegidas
- Obtención del usuario autenticado

### Sistema de mensajes

- Enviar mensajes
- Bandeja de entrada (Inbox)
- Bandeja de enviados (Sent)
- Papelera (Trash)
- Restaurar mensajes

---

##  Endpoints principales

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| POST | `/api/auth/register` | Crear usuario |
| POST | `/api/auth/login` | Iniciar sesión |
| GET | `/api/me` | Usuario autenticado |
| POST | `/api/message` | Enviar mensaje |
| GET | `/api/message?box=inbox` | Inbox |
| GET | `/api/message?box=sent` | Enviados |
| GET | `/api/message?box=trash` | Papelera |
| PUT | `/api/message/{id}/trash` | Mover a papelera |
| PUT | `/api/message/{id}/restore` | Restaurar mensaje |

---

##  Modelo de datos

### Users

| Campo | Tipo |
|------|------|
| id | UUID |
| email | VARCHAR |
| password_hash | VARCHAR |
| created_at | TIMESTAMP |

### Messages

| Campo | Tipo |
|------|------|
| id | UUID |
| from_user | UUID |
| to_user | UUID |
| subject | VARCHAR |
| body | TEXT |
| is_read | BOOLEAN |
| is_trashed | BOOLEAN |
| created_at | TIMESTAMP |

---

##  Estructura del proyecto

```text
mail-system/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── database.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── src/
    │   ├── views/
    │   ├── stores/
    │   ├── router/
    │   ├── services/
    │   └── App.vue
    └── package.json
```

---

## ⚙ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/mail-system.git
cd mail-system
```

### 2. Backend

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Crear el archivo `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/maildb
SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Ejecutar la API:

```bash
uvicorn app.main:app --reload
```

Documentación Swagger:

```text
http://127.0.0.1:8000/docs
```

---

### 3. Frontend

```bash
cd frontend

npm install
npm run dev
```

Aplicación:

```text
http://localhost:5173
```

---

##  Flujo de autenticación

1. El usuario inicia sesión.
2. FastAPI valida las credenciales.
3. Se genera un **JWT**.
4. Pinia almacena el token.
5. Axios agrega automáticamente:

```http
Authorization: Bearer <token>
```

6. Las rutas protegidas validan el usuario mediante JWT.

---

##  Pruebas realizadas

Se validó la API mediante **Postman**:

- Registro de usuarios
- Login y generación de JWT
- Consulta del usuario autenticado
- Envío de mensajes
- Bandeja Inbox
- Bandeja Sent
- Papelera
- Restauración de mensajes

---

##  Estado del proyecto

### Backend

- [x] Autenticación JWT
- [x] Registro de usuarios
- [x] Login
- [x] Rutas protegidas
- [x] CRUD de mensajes
- [x] Inbox
- [x] Sent
- [x] Trash
- [x] Restore

### Frontend

- [x] Proyecto Vue 3
- [x] Pinia
- [x] Vue Router
- [x] Login conectado a la API
- [ ] Inbox UI
- [ ] Sent UI
- [ ] Trash UI
- [ ] Redacción de mensajes

---

##  Próximas mejoras

- Interfaz completa de correo
- Marcar mensajes como leídos
- Eliminación permanente
- Búsqueda de mensajes
- Paginación
- Docker Compose
- Alembic para migraciones
- Despliegue en la nube

---

##  Autor

**Rubén Abimalec Caballero Sánchez**

Ingeniería en Sistemas Computacionales  
Backend • FastAPI • Vue • PostgreSQL • REST APIs
