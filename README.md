# 🎬 Cinema Web - Sistema de Venta de Entradas

Sistema completo de venta de entradas de cine con panel administrativo, carrito de compras y gestión de funciones.

## 📋 Características principales

✅ **Autenticación y RBAC**
- Login/Logout con sesiones persistentes
- Roles: Usuario y Administrador
- Protección de rutas con decoradores `@login_required` y `@admin_required`

✅ **Gestión de Películas**
- CRUD completo de películas
- Asociación con géneros y actores
- Carátulas, sinopsis, duración, clasificación

✅ **Sistema de Funciones**
- Programación de proyecciones por sala y horario
- Validación automática de conflictos (sin funciones superpuestas)
- Cálculo automático de `hora_fin` basado en duración de película
- Soporte para múltiples formatos (DOB, 3D, Subtitulado)

✅ **Compra de Entradas**
- Selección de asientos (estándar, premium, VIP)
- Carrito de compras temporal
- Código QR para cada ticket
- Historial de compras

✅ **Panel Administrativo Moderno**
- Dashboard con estadísticas en tiempo real
- Gestión de películas, funciones, géneros, actores
- Gestión de usuarios (convertir a admin, eliminar)
- Interfaz responsiva con diseño moderno

## 🛠 Tecnologías

- **Backend:** Python 3 + Flask
- **Base de datos:** MySQL 8
- **Frontend:** HTML5 + CSS3 + JavaScript Vanilla
- **Autenticación:** bcrypt
- **Email:** Flask-Mail (Gmail SMTP)
- **Códigos QR:** qrcode + Pillow

## 📦 Instalación

### Requisitos previos
- Python 3.8+
- MySQL 8.0+
- pip (gestor de paquetes Python)

### Pasos de instalación

```bash
# 1. Clonar repositorio
git clone <tu-repo>
cd cinema-web

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
# Editar config.py con tus credenciales MySQL
# Luego ejecutar el script SQL:
mysql -u root -p cinema < cinema.sql

# 5. Ejecutar la aplicación
python app.py
```

Accede en: `http://localhost:5000`

**Credenciales de prueba:**
- Email: `admin@cinevox.com`
- Contraseña: (verificar en base de datos)

## 🚀 Despliegue a Railway

### Variables de entorno necesarias

En el dashboard de Railway, configura:

```env
DB_HOST=tu-host-mysql
DB_PORT=3306
DB_USER=tu-usuario-mysql
DB_PASSWORD=tu-password
DB_NAME=cinema
FLASK_ENV=production
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-app-password
```

### Stack en Railway

- **Database:** MySQL 8
- **Web Service:** Python (auto-detecta `Procfile`)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** gunicorn app:app

## 📁 Estructura del proyecto

```
cinema-web/
├── app.py                 # Aplicación principal Flask
├── db.py                  # Funciones de base de datos
├── config.py              # Configuración (credenciales, email)
├── cinema.sql             # Script de inicialización de BD
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración para Railway
├── static/
│   ├── css/styles.css
│   └── js/main.js
└── templates/
    ├── index.html        # Página principal
    ├── login.html
    ├── mi_cuenta.html    # Historial de compras
    └── admin/            # Panel administrativo
        ├── base.html
        ├── dashboard.html
        ├── peliculas.html
        ├── funciones.html
        ├── generos.html
        ├── actores.html
        └── usuarios.html
```

## 🔑 Rutas principales

### Públicas
- `GET /` - Página principal con películas
- `GET /login` - Formulario de login
- `POST /login` - Procesar login
- `GET /logout` - Cerrar sesión
- `GET /mi_cuenta` - Historial de compras del usuario

### API (requieren autenticación)
- `GET /api/peliculas` - Listado de películas
- `GET /api/funciones` - Funciones disponibles
- `GET /api/asientos/<funcion_id>` - Asientos de una función
- `POST /api/procesar-compra` - Crear pedido
- `POST /api/verificar-ticket` - Validar ticket con QR

### Admin (requieren rol admin)
- `GET /admin/` - Dashboard
- `GET /admin/peliculas` - Listar películas
- `POST /admin/peliculas/crear` - Crear película
- `GET /admin/usuarios` - Gestión de usuarios
- `POST /admin/usuarios/<id>/convertir-admin` - Promover a admin

## 💾 Base de datos

**Tablas principales:**
- `usuarios` - Usuarios del sistema (rol: usuario|admin)
- `peliculas` - Catálogo de películas
- `funciones` - Proyecciones programadas
- `asientos` - Asientos de salas
- `tiquetes` - Entradas vendidas
- `generos`, `actores` - Metadatos

Véase `DOCUMENTACION_TECNICA.md` para detalles completos del esquema.

## 🔒 Seguridad

✅ Contraseñas hasheadas con bcrypt
✅ Validación de sesiones persistentes
✅ Protección CSRF implied (Flask sessions)
✅ Validación de conflictos de horarios en BD
✅ Restricción de acceso por rol

## 📝 Licencia

Proyecto de demostración - Sin licencia especificada

## 👤 Autor

Jerson David Silva - dev.daviar@gmail.com

---

**Última actualización:** 15 de abril de 2026
