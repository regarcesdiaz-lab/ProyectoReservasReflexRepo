# 🌴 TurismoDO — Plataforma de Reservas y Ofertas Turísticas

Aplicación web full-stack desarrollada con **Reflex (Python)** que permite gestionar reservas y publicar ofertas turísticas. Incluye **autenticación de usuarios** (admin y clientes), **panel de administración** completo, **API REST** y conexión a **MySQL en la nube (Aiven)**.

> 🎓 Proyecto Final — Desarrollo Web


---

## ✨ Funcionalidades

### 👤 Para clientes
- Registro y login con email/contraseña (contraseñas encriptadas con bcrypt)
- Búsqueda de ofertas turísticas por destino
- Ver detalle completo de cada oferta (descripción, itinerario, qué incluye)
- Crear reservas con datos precargados
- Página "Mis reservas" con historial y estado
- Envío de sugerencias desde la sección Contacto

### 🛡️ Para administradores
- **Dashboard** con estadísticas (reservas, ofertas, sugerencias)
- **Gestión de reservas**: filtrar por estado, confirmar, cancelar y eliminar
- **Gestión de ofertas**: crear, editar, activar/desactivar y eliminar
- **Gestión de sugerencias**: ver mensajes, marcar como leídas, eliminar

### 🔌 API REST
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/ofertas` | Listar todas las ofertas activas |
| GET | `/api/ofertas/{id}` | Detalle de una oferta |
| POST | `/api/reservas` | Crear nueva reserva |
| GET | `/api/reservas` | Listar todas las reservas |
| GET | `/api/sugerencias` | Listar mensajes recibidos |

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend + Backend | Reflex 0.8 (Python puro) |
| Base de datos | MySQL 8 (Aiven Cloud) |
| ORM y migraciones | SQLModel + Alembic |
| API REST | FastAPI (integrado) |
| Autenticación | bcrypt + passlib |
| Despliegue | Render |
| Control de versiones | Git + GitFlow + GitHub |

---

## 📂 Estructura del proyecto
```bash
ProyectoReservasReflex/
├── assets/images/
├── ProyectoReservasReflex/
│   ├── ProyectoReservasReflex.py    # Entrada principal
│   ├── models/                      # Usuario, Oferta, Reserva, Sugerencia
│   ├── states/                      # Lógica de estado de cada página
│   ├── pages/                       # 7 páginas (incluye /admin)
│   ├── components/                  # navbar, footer, oferta_card
│   ├── utils/                       # auth.py (hash de contraseñas)
│   └── api/endpoints.py             # API REST
├── alembic/                         # Migraciones de BD
├── .env                             # Variables de entorno (no se sube)
├── .env.example                     # Plantilla
├── ca.pem                           # Certificado SSL de Aiven (no se sube)
├── .gitignore
├── rxconfig.py
├── requirements.txt
├── seed.py                          # Datos de prueba
└── README.md
````
---

## ⚙️ Instalación local

### Requisitos previos
- Python 3.10 o superior
- Git
- Una cuenta gratuita en [Aiven.io](https://aiven.io) (para MySQL en la nube)

### Pasos

**1. Clonar el repositorio**
```bash
git clone https://github.com/regarcesdiaz-lab/ProyectoReservasReflexRepo.git
cd ProyectoReservasReflex
```

**2. Crear entorno virtual e instalar dependencias**
```bash
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # Mac/Linux
pip install -r requirements.txt
```

**3. Crear la base de datos MySQL en Aiven**

a) Regístrate en [https://aiven.io](https://aiven.io)
b) Click en **"Create service"** → selecciona **MySQL**
c) Elige el plan **Free (Hobbyist)** y una región cercana
d) Espera 2-5 minutos hasta que el estado sea **"Running"** (verde)

**4. Obtener credenciales de Aiven**

Una vez creado el servicio, ve a **Overview** y copia:
- **Host** (ej. `turismodo-mysql-xxx.aivencloud.com`)
- **Port** (ej. `12026`)
- **User** (`avnadmin`)
- **Password** (click en el ojito 👁️ para revelarla)
- **Database name** (`defaultdb`)

**5. Descargar el certificado SSL**

En la misma pantalla, click en **Download CA certificate** (`ca.pem`).
Cópialo a la **raíz del proyecto** (junto a `rxconfig.py`).

**6. Configurar variables de entorno**

Crea tu archivo `.env` a partir de la plantilla:
```bash
copy .env.example .env           # Windows
cp .env.example .env             # Mac/Linux
```

Ábrelo y reemplaza con tus credenciales reales de Aiven:
```env
DATABASE_URL=mysql+pymysql://avnadmin:@tu contraseña@tu-Host:TU_PUERTO/defaultdb?ssl_ca=ca.pem
API_URL=http://localhost:8000
SECRET_KEY=cambia-esta-clave-en-produccion-12345
```

**7. Verificar la conexión a Aiven**
```bash
python -c "from dotenv import load_dotenv; load_dotenv(); import os; from sqlalchemy import create_engine, text; engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('CONEXION OK:', conn.execute(text('SELECT 1')).scalar()); conn.close()"
```

Debe imprimir: `CONEXION OK: 1`

**8. Inicializar Reflex y migrar la BD**
```bash
reflex init                                              # elige plantilla 0 (blank)
reflex db init
reflex db makemigrations --message "modelos iniciales"
reflex db migrate
```

**9. Cargar datos de prueba**
```bash
python seed.py
```
Responde **s** a las preguntas para crear los usuarios y las 6 ofertas turísticas.

**10. Correr la aplicación**
```bash
reflex run
```

Abre en tu navegador:
- 🌐 App: http://localhost:3000
- 📘 API Swagger: http://localhost:8000/docs

---

## 🔐 Cuentas de prueba

Después de ejecutar `python seed.py`, puedes iniciar sesión con:

| Rol | Email | Contraseña |
|-----|-------|------------|
| 👑 Admin | `admin@turismodo.com` | `admin123` |
| 👤 Cliente | `cliente@test.com` | `cliente123` |

> ⚠️ Cambia estas credenciales antes de desplegar en producción.

---

## 🗺️ Rutas de la aplicación

| Ruta | Acceso | Descripción |
|------|--------|-------------|
| `/` | Público | Página de inicio (ofertas + contacto) |
| `/oferta/[id]` | Público | Detalle de una oferta |
| `/registro` | Público | Crear cuenta de cliente |
| `/login` | Público | Iniciar sesión |
| `/reservas?oferta=ID` | Cliente | Formulario de reserva |
| `/mis-reservas` | Cliente | Ver reservas propias |
| `/admin` | Admin | Panel de administración |

---

## ☁️ Ventajas de usar Aiven (en la nube)

A diferencia de XAMPP local, al usar Aiven los datos viven en la nube. Esto significa:
- ✅ La base de datos siempre está disponible
- ✅ Cualquier dispositivo puede conectarse (con el `.env` correcto)
- ✅ Los datos persisten aunque se reinicie tu PC
- ✅ Es indispensable para el despliegue en Render

---

## 🌿 Flujo de trabajo con GitFlow

| Rama | Propósito |
|------|-----------|
| `main` | Código en producción |
| `develop` | Integración de features |
| `feature/*` | Nuevas funcionalidades |
| `release/*` | Preparación de release |
| `hotfix/*` | Correcciones urgentes |

**Ejemplo de uso:**
```bash
git checkout develop
git checkout -b feature/nueva-funcionalidad
# trabajar...
git push origin feature/nueva-funcionalidad
# Pull Request hacia develop en GitHub
```

---

## 🚢 Despliegue en Render

Como la BD ya está en Aiven, no necesitas crearla en Render. Solo subes la app:

### 1. Crear Web Service en Render
- Conecta tu repo de GitHub en https://render.com
- **Build Command:** `pip install -r requirements.txt && reflex db migrate`
- **Start Command:** `reflex run --env prod`
- **Environment Variables:**
  - `DATABASE_URL` → la misma URL de Aiven (con `?ssl_ca=ca.pem`)
  - `API_URL` → la URL que Render te asigne
  - `PYTHON_VERSION` → `3.11`

### 2. Subir el certificado SSL
Como `ca.pem` no se sube a GitHub (por seguridad), tienes dos opciones:
- **Opción A**: Configurar Aiven para no requerir SSL (menos seguro)
- **Opción B**: Modificar la cadena de conexión para usar SSL sin archivo CA específico

---

## 🧪 Probar la API REST

Ejemplo con `curl` para crear una reserva:
```bash
curl -X POST http://localhost:8000/api/reservas \
  -H "Content-Type: application/json" \
  -d '{
    "oferta_id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@email.com",
    "telefono": "+18095550123",
    "cantidad_personas": 2,
    "fecha_viaje": "2026-08-15",
    "metodo_pago": "tarjeta"
  }'
```

---

## 🔒 Archivos sensibles

Estos archivos NO se suben a GitHub (están en `.gitignore`):
- `.env` — contiene la contraseña de Aiven
- `ca.pem` — certificado SSL de Aiven
- `venv/` — entorno virtual local
- `.web/` — build generado por Reflex
- `reflex.db` — base de datos SQLite local (solo para pruebas)

**Para colaborar o entregar el proyecto**, comparte el `.env` y `ca.pem` por un canal privado (correo, mensaje directo), no por GitHub.

---

## 👤 Autor

**Ramón Garcés**
Curso: 5to A inofrmatica
Año: 2026

---

## 🔗 Enlaces útiles

- 📘 [Reflex docs](https://reflex.dev/docs)
- 📗 [SQLModel](https://sqlmodel.tiangolo.com/)
- 📕 [FastAPI](https://fastapi.tiangolo.com/)
- 🚀 [Render](https://render.com/docs)
- 💾 [Aiven MySQL](https://aiven.io/mysql)
- 🔀 [Atlassian GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

---

## 📄 Licencia

Proyecto académico — uso libre con atribución al autor.

## 🔗 Enlaces útiles

- [Reflex docs](https://reflex.dev/docs)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Render](https://render.com/docs)
- [Aiven MySQL](https://aiven.io/mysql)
