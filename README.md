# 🌴 Plataforma de Reservas y Ofertas Turísticas

Aplicación web full-stack con **Reflex (Python)**, **MySQL** y **API REST**, con sistema de **autenticación** (admin y clientes) y panel de administración completo.

> Proyecto Final – Desarrollo Web

---

## ✨ Características

### 👤 Para usuarios (clientes):
- Registro y login con email/contraseña
- Ver ofertas turísticas con búsqueda
- Detalle completo de cada oferta (descripción, itinerario, incluye)
- Crear reservas (con sus datos precargados)
- Ver historial de "Mis reservas" con estado
- Enviar sugerencias/mensajes desde la sección Contacto

### 🛡️ Para administradores:
- Dashboard con estadísticas
- **Gestión de reservas**: ver todas, filtrar por estado, confirmar, cancelar, eliminar
- **Gestión de ofertas**: crear, editar, activar/desactivar, eliminar
- **Gestión de sugerencias**: ver mensajes, marcar leídas, eliminar

### 🔌 API REST:
- `GET /api/ofertas` — listar ofertas activas
- `GET /api/ofertas/{id}` — detalle de oferta
- `POST /api/reservas` — crear reserva
- `GET /api/reservas` — listar reservas
- `GET /api/sugerencias` — listar sugerencias

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend + Backend | Reflex 0.6+ (Python puro) |
| Base de datos | MySQL 8 |
| ORM | SQLModel |
| Migraciones | Alembic |
| API REST | FastAPI (integrado) |
| Auth | bcrypt + passlib |
| Despliegue | Render |
| Control de versiones | Git + GitFlow |

---

## 📂 Estructura del proyecto

```
ProyectoReservasReflex/
├── assets/images/
├── ProyectoReservasReflex/
│   ├── ProyectoReservasReflex.py   # entrada principal
│   ├── models/                     # Usuario, Oferta, Reserva, Sugerencia
│   ├── states/                     # Lógica: auth, admin, ofertas, etc.
│   ├── pages/                      # 7 páginas (incluyendo /admin)
│   ├── components/                 # navbar, footer, oferta_card
│   ├── utils/                      # auth.py (hash de contraseñas)
│   └── api/endpoints.py            # API REST
├── alembic/                        # migraciones (auto)
├── .env.example
├── .gitignore
├── rxconfig.py
├── requirements.txt
├── seed.py                         # datos de prueba + usuarios
└── README.md
```

---

## ⚙️ Instalación local

### Requisitos previos
- Python 3.10+
- MySQL 8 (XAMPP recomendado)
- Git

### Pasos

1. **Clonar y entrar al proyecto**
   ```bash
   git clone https://github.com/regarcesdiaz-lab/ProyectoReservasReflexRepo.git
   cd ProyectoReservasReflex
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate            # Windows
   source venv/bin/activate         # Mac/Linux
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crear base de datos en MySQL**
   En phpMyAdmin (http://localhost/phpmyadmin) crea una base llamada `reservas_turisticas` con cotejamiento `utf8mb4_unicode_ci`.

5. **Configurar variables de entorno**
   ```bash
   copy .env.example .env           # Windows
   cp .env.example .env             # Mac/Linux
   ```
   Edita `.env` y ajusta `DATABASE_URL` según tu MySQL.

6. **Inicializar y migrar la BD**
   ```bash
   reflex init                      # elige plantilla 0 (blank)
   reflex db init
   reflex db makemigrations --message "inicial"
   reflex db migrate
   ```

7. **Cargar datos de prueba**
   ```bash
   python seed.py
   ```

8. **Correr la app**
   ```bash
   reflex run
   ```

   - App: http://localhost:3000
   - API Swagger: http://localhost:8000/docs

---

## 🔐 Cuentas de prueba

Después de correr `python seed.py`, puedes iniciar sesión con:

| Rol | Email | Contraseña |
|-----|-------|------------|
| **Admin** | admin@turismodo.com | admin123 |
| **Cliente** | cliente@test.com | cliente123 |

⚠️ Cambia estas credenciales en producción.

---

## 🗺️ Rutas de la aplicación

| Ruta | Acceso | Descripción |
|------|--------|-------------|
| `/` | Público | Página de inicio con ofertas y contacto |
| `/oferta/[id]` | Público | Detalle de una oferta |
| `/registro` | Público | Crear cuenta de cliente |
| `/login` | Público | Iniciar sesión |
| `/reservas?oferta=ID` | Cliente | Formulario de reserva |
| `/mis-reservas` | Cliente | Ver sus propias reservas |
| `/admin` | Admin | Panel de administración |

---

## 🌿 GitFlow

- `main` — producción estable
- `develop` — integración de features
- `feature/*` — nuevas funcionalidades
- `release/*` — preparación de release
- `hotfix/*` — arreglos urgentes

```bash
git checkout develop
git checkout -b feature/nombre
# trabajar...
git push origin feature/nombre
# Pull Request hacia develop
```

---

## 🚢 Despliegue en Render

1. Crea MySQL en Aiven (gratis) o Railway
2. Conecta tu repo en Render → New Web Service
3. Build Command: `pip install -r requirements.txt && reflex db migrate`
4. Start Command: `reflex run --env prod`
5. Env Vars: `DATABASE_URL`, `API_URL`, `PYTHON_VERSION=3.11`

---

## 👤 Autor

**[Ramon Eduardo Garces Diaz]**
Curso: Desarrollo Web — 2026

---

## 🔗 Enlaces útiles

- [Reflex docs](https://reflex.dev/docs)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Render](https://render.com/docs)
- [Aiven MySQL](https://aiven.io/mysql)
