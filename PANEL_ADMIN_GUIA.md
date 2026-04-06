# GUÍA: PANEL ADMINISTRATIVO DEL CINE

## 📌 RESUMEN EJECUTIVO

Panel web para que el gerente/dueño gestione todo el cine sin programar.
---

## 🎯 FUNCIONALIDADES PRINCIPALES

### 1. **AUTENTICACIÓN (Login)**
El admin necesita usuario y contraseña para entrar.

**Endpoints:**
```
GET  /admin/login              → Formulario de login
POST /admin/login              → Procesar credenciales
GET  /admin/logout             → Cerrar sesión
```

**Flujo:**
```
1. Admin entra a /admin/login
2. Ingresa email + contraseña
3. System valida en tabla ADMINS
4. Si OK → Redirige a /admin/dashboard
5. Si error → Muestra mensaje de error
```

---

### 2. **DASHBOARD (Página principal)**
Resumen visual de lo que pasa en el cine HOY.

**Endpoint:**
```
GET /admin/dashboard
```

**Debe mostrar:**
```
┌─────────────────────────────┐
│ CINEVOX - DASHBOARD ADMIN   │
├─────────────────────────────┤
│                             │
│ 💰 INGRESOS HOY             │
│    $1,250.00                │
│                             │
│ 🎬 PELÍCULAS ACTIVAS        │
│    1 película               │
│                             │
│ 👥 ENTRADAS VENDIDAS        │
│    47 entradas              │
│                             │
│ 📊 OCUPACIÓN DE SALA        │
│    47/180 asientos (26%)    │
│                             │
│ 📅 PRÓXIMAS FUNCIONES       │
│    ├─ 14:30 - IMAX          │
│    ├─ 17:15 - Premium       │
│    └─ 20:00 - Sala 3        │
│                             │
└─────────────────────────────┘
```

**SQL a ejecutar:**
```sql
-- Total vendido HOY
SELECT SUM(total) FROM tiquetes 
WHERE DATE(fecha_compra) = CURDATE();

-- Películas activas
SELECT COUNT(*) FROM peliculas 
WHERE estado = 'activa';

-- Entradas vendidas HOY
SELECT COUNT(*) FROM tiquetes 
WHERE DATE(fecha_compra) = CURDATE();

-- Ocupación actual
SELECT COUNT(*) FROM detalle_tiquete 
WHERE funcion_id IN (
  SELECT id FROM funciones 
  WHERE DATE(fecha) = CURDATE()
);
```

---

### 3. **GESTIONES DE PELÍCULAS (CRUD)**

#### Ver todas las películas
**Endpoint:**
```
GET /admin/peliculas
```

**Muestra tabla:**
```
┌──────────────────────────────────────────┐
│ PELÍCULAS                                │
├──────────────────────────────────────────┤
│ ID │ TÍTULO           │ AÑO │ DIRECTOR │
├────┼──────────────────┼─────┼──────────┤
│ 1  │ Spider-Man       │2026 │ Destin   │
│    │ [Editar][Eliminar]                 │
├────┴──────────────────┴─────┴──────────┤
│                                          │
│ [+ AGREGAR NUEVA PELÍCULA]               │
└──────────────────────────────────────────┘
```

#### Agregar película
**Endpoints:**
```
GET  /admin/peliculas/crear      → Mostrar formulario
POST /admin/peliculas            → Guardar en BD
```

**Formulario tiene:**
```
- Título (texto)
- Descripción (textarea)
- Duración en minutos (número)
- Clasificación: PG-13, R, +15, +18 (select)
- Año (número)
- Director (texto)
- Tagline / Frase promocional (texto)
- Calificación 1-10 (número)
- URL de imagen (texto)
- Estado: activa/próxima/finalizada (select)

[GUARDAR] [CANCELAR]
```

**Code:**
```python
@app.route('/admin/peliculas/crear', methods=['GET', 'POST'])
@login_required
def crear_pelicula():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO peliculas 
            (titulo, descripcion, duracion, clasificacion, anio, director, tagline, puntuacion, imagen_url, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form['titulo'],
            request.form['descripcion'],
            request.form['duracion'],
            request.form['clasificacion'],
            request.form['anio'],
            request.form['director'],
            request.form['tagline'],
            request.form['puntuacion'],
            request.form['imagen_url'],
            request.form['estado']
        ))
        conn.commit()
        return redirect('/admin/peliculas')
    
    return render_template('admin/peliculas_form.html')
```

#### Editar película
**Endpoints:**
```
GET  /admin/peliculas/{id}/editar     → Mostrar formulario pre-llenado
POST /admin/peliculas/{id}            → Guardar cambios
```

#### Eliminar película
**Endpoint:**
```
POST /admin/peliculas/{id}/eliminar   → Borrar de BD
```

**⚠️ Advertencia:** Si la película tiene funciones activas, mostrar error.

---

### 4. **GESTIÓN DE FUNCIONES (CRUD)**

#### Ver todas las funciones
**Endpoint:**
```
GET /admin/funciones
```

**Muestra tabla:**
```
┌──────────────────────────────────────────────────┐
│ FUNCIONES                                        │
├──────────────────────────────────────────────────┤
│ ID │ PELÍCULA    │ FECHA      │ HORA  │ VENDIDAS│
├────┼─────────────┼────────────┼───────┼─────────┤
│ 1  │ Spider-Man  │ 31/03/2026 │ 14:30 │ 12/180  │
│    │ Sala: IMAX, Precio: $18.50                 │
│    │ [Editar][Eliminar]                         │
├────┴─────────────┴────────────┴───────┴─────────┤
│                                                  │
│ [+ AGREGAR NUEVA FUNCIÓN]                        │
└──────────────────────────────────────────────────┘
```

#### Agregar función
**Endpoints:**
```
GET  /admin/funciones/crear     → Formulario
POST /admin/funciones           → Guardar
```

**Formulario:**
```
- Película: [Dropdown con todas las películas]
- Fecha: [Date picker]
- Hora: [Time picker]
- Sala: [Dropdown: Sala 1, 2, 3, IMAX, Premium]
- Precio: [Número]
- Tecnología: [Dropdown: 2D, IMAX 4K, Dolby Vision]

[GUARDAR] [CANCELAR]
```

#### Editar función
```
GET  /admin/funciones/{id}/editar
POST /admin/funciones/{id}
```

#### Eliminar función
```
POST /admin/funciones/{id}/eliminar
```

**⚠️ Advertencia:** Si hay entradas vendidas, mostrar error.

---

### 5. **REPORTE DE VENTAS**

**Endpoint:**
```
GET /admin/ventas
```

**Muestra:**
```
┌────────────────────────────────────────────────────┐
│ VENTAS REGISTRADAS                               │
├────────────────────────────────────────────────────┤
│                                                    │
│ [Filtrar por fecha] [Desde: ___] [Hasta: ___]    │
│ [Filtrar por estado] [Activo] [Canjeado]         │
│ [Buscar email] [_______________________________]  │
│ [BUSCAR]                                          │
│                                                    │
├────────────────────────────────────────────────────┤
│ EMAIL              │ PELÍCULA   │ ASIENTOS │ TOTAL│
├────────────────────┼────────────┼──────────┼─────┤
│user@example.com    │Spider-Man  │C5,C6,C7  │$46.0│
│Estado: ACTIVO | Fecha: 01/04 | [Ver] [PDF]      │
│                                                    │
│dsadsa@dsa.dsa    │Spider-Man  │A4        │$12.5│
│Estado: CANJEADO | Fecha: 01/04 | [Ver]           │
│                                                    │
└────────────────────────────────────────────────────┘
```

**Code:**
```python
@app.route('/admin/ventas')
@login_required
def admin_ventas():
    fecha_desde = request.args.get('desde')
    fecha_hasta = request.args.get('hasta')
    estado = request.args.get('estado')
    email = request.args.get('email')
    
    query = "SELECT * FROM tiquetes WHERE 1=1"
    params = []
    
    if fecha_desde:
        query += " AND DATE(fecha_compra) >= %s"
        params.append(fecha_desde)
    
    if fecha_hasta:
        query += " AND DATE(fecha_compra) <= %s"
        params.append(fecha_hasta)
    
    if estado:
        query += " AND estado = %s"
        params.append(estado)
    
    if email:
        query += " AND email LIKE %s"
        params.append(f"%{email}%")
    
    query += " ORDER BY fecha_compra DESC"
    
    conn = get_db_connection()
    ventas = conn.query(query, params)
    
    return render_template('admin/ventas.html', ventas=ventas)
```

---

### 6. **REPORTES (ESTADÍSTICAS Y GRÁFICOS)**

**Endpoint:**
```
GET /admin/reportes
```

**Muestra:**
```
┌──────────────────────────────────┐
│ REPORTES ESTADÍSTICOS            │
├──────────────────────────────────┤
│                                  │
│ 📈 GRÁFICO: VENTAS ÚLTIMOS 7 DÍAS│
│    [Gráfico de barras]           │
│    Lun: $180                     │
│    Mar: $250                     │
│    ...                           │
│                                  │
│ 💵 INGRESOS POR TIPO ASIENTO    │
│    Estándar: $450 (36 vendidas)  │
│    Premium:  $675 (45 vendidas)  │
│    VIP:      $925 (50 vendidas)  │
│                                  │
│ 👥 FUNCIONES CON MÁS OCUPACIÓN  │
│    1. 31/03 14:30 → 67%          │
│    2. 02/04 15:00 → 42%          │
│    3. 01/04 17:15 → 38%          │
│                                  │
│ [📥 Descargar Excel]             │
│                                  │
└──────────────────────────────────┘
```

**SQL:**
```sql
-- Ventas por día (últimos 7 días)
SELECT DATE(fecha_compra) as fecha, SUM(total) as total
FROM tiquetes
WHERE fecha_compra >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(fecha_compra)
ORDER BY fecha DESC;

-- Ingresos por tipo asiento
SELECT ta.nombre, COUNT(dt.id) as cantidad, SUM(ta.precio) as total
FROM detalle_tiquete dt
JOIN asientos a ON dt.asiento_id = a.id
JOIN tipos_asientos ta ON a.tipo_id = ta.id
GROUP BY ta.nombre;

-- Ocupación por función
SELECT f.id, p.titulo, f.fecha, f.hora, 
       COUNT(dt.id) as ocupados,
       (COUNT(dt.id) * 100 / 180) as porcentaje
FROM funciones f
LEFT JOIN detalle_tiquete dt ON f.id = dt.funcion_id
LEFT JOIN peliculas p ON f.pelicula_id = p.id
GROUP BY f.id
ORDER BY f.fecha DESC, f.hora DESC;
```

**Para gráficos usar:** Chart.js (librería JavaScript)

---

### 7. **GESTIÓN DE ASIENTOS**

**Endpoint:**
```
GET /admin/asientos?funcion_id=1
```

**Muestra mapa visual:**
```
┌─────────────────────────────────┐
│ ASIENTOS - Función: 31/03 14:30 │
├─────────────────────────────────┤
│                                 │
│ FILA A:  [✅][✅][❌][✅][✅]... │
│ FILA B:  [❌][❌][✅][✅][✅]... │
│ FILA C:  [✅][❌][✅][❌][✅]... │
│ ...                             │
│                                 │
│ ✅ = Disponible  ❌ = Ocupado    │
│                                 │
│ (Clickear en disponible para    │
│  liberar manualmente si es req) │
│                                 │
└─────────────────────────────────┘
```

**Code HTML:**
```html
<div class="seat-grid">
    {% for seat in seats %}
        <button class="seat {% if seat.estado == 'disponible' %}available{% else %}occupied{% endif %}"
                onclick="toggleSeat({{ seat.id }})">
            {{ seat.numero }}
        </button>
    {% endfor %}
</div>
```

---

### 8. **CONFIGURACIÓN**

**Endpoint:**
```
GET /admin/config
```

**Formularios:**

#### A. Cambiar precios
```
Precio Estándar:  $[12.50] [ACTUALIZAR]
Precio Premium:   $[15.00] [ACTUALIZAR]
Precio VIP:       $[18.50] [ACTUALIZAR]
```

#### B. Cambiar contraseña
```
Contraseña actual: [_______]
Nueva contraseña:  [_______]
Confirmar:         [_______]

[CAMBIAR CONTRASEÑA]
```

#### C. Credenciales de email
```
Servidor SMTP:     [smtp.gmail.com] [ACTUALIZAR]
Usuario:           [tu@gmail.com]   [ACTUALIZAR]
Contraseña app:    [____________]   [ACTUALIZAR]
```

---

## 🗂️ ESTRUCTURA DE CARPETAS

```
templates/
├── admin/                 ← NUEVA CARPETA
│   ├── base.html         (Template base con sidebar)
│   ├── login.html
│   ├── dashboard.html
│   ├── peliculas_list.html
│   ├── peliculas_form.html
│   ├── funciones_list.html
│   ├── funciones_form.html
│   ├── ventas.html
│   ├── asientos.html
│   ├── reportes.html
│   └── config.html
│
static/
├── css/
│   └── admin.css         (Estilos del panel admin)
│
├── js/
│   └── admin.js          (Lógica del admin, gráficos)
```

---

## 🔐 BASE DE DATOS: TABLA ADMINS

```sql
CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP NULL
);

-- Insertar admin inicial
INSERT INTO admins (email, password_hash, nombre)
VALUES ('admin@cinevox.com', '[hash_de_contraseña]', 'Administrador');
```

---

## 📦 DEPENDENCIAS A INSTALAR

```bash
pip install flask-login          # Autenticación
pip install werkzeug.security    # Hash de contraseñas (ya viene con Flask)
pip install openpyxl             # Exportar Excel
```

Agregar a `requirements.txt`:
```
Flask-Login==0.6.2
openpyxl==3.10.0
```

---

## 🏗️ CODE ARCHITECTURE

### 1. Crear base_admin.html
```html
<!DOCTYPE html>
<html>
<head>
    <title>Admin - CINEVOX</title>
    <link rel="stylesheet" href="/static/css/admin.css">
</head>
<body>
    <div class="admin-container">
        <!-- SIDEBAR -->
        <nav class="sidebar">
            <div class="logo">CINEVOX ADMIN</div>
            <ul>
                <li><a href="/admin/dashboard">Dashboard</a></li>
                <li><a href="/admin/peliculas">Películas</a></li>
                <li><a href="/admin/funciones">Funciones</a></li>
                <li><a href="/admin/ventas">Ventas</a></li>
                <li><a href="/admin/reportes">Reportes</a></li>
                <li><a href="/admin/asientos">Asientos</a></li>
                <li><a href="/admin/config">Configuración</a></li>
                <li><a href="/admin/logout" class="logout">Cerrar Sesión</a></li>
            </ul>
        </nav>
        
        <!-- MAIN CONTENT -->
        <main class="main-content">
            {% block content %}{% endblock %}
        </main>
    </div>
</body>
</html>
```

### 2. Crear app.py con rutas admin
```python
from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tu-clave-secreta')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# ========== RUTAS PÚBLICAS (Usuario) ==========
@app.route('/')
def home():
    return render_template('index.html')

# ========== RUTAS ADMIN ==========

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validar credenciales (aquí conectar a BD)
        # Si OK, crear sesión
        session['admin_email'] = email
        return redirect('/admin/dashboard')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_email', None)
    return redirect('/admin/login')

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Calcular estadísticas
    conn = get_db_connection()
    
    total_hoy = conn.query("SELECT SUM(total) FROM tiquetes WHERE DATE(fecha_compra) = CURDATE()")[0][0]
    peliculas_activas = conn.query("SELECT COUNT(*) FROM peliculas WHERE estado = 'activa'")[0][0]
    entradas_hoy = conn.query("SELECT COUNT(*) FROM tiquetes WHERE DATE(fecha_compra) = CURDATE()")[0][0]
    ocupacion = conn.query("SELECT COUNT(*) FROM detalle_tiquete")[0][0]
    
    return render_template('admin/dashboard.html',
        total_hoy=total_hoy,
        peliculas_activas=peliculas_activas,
        entradas_hoy=entradas_hoy,
        ocupacion=ocupacion
    )

@app.route('/admin/peliculas')
@login_required
def admin_peliculas():
    conn = get_db_connection()
    peliculas = conn.query("SELECT * FROM peliculas ORDER BY titulo")
    return render_template('admin/peliculas_list.html', peliculas=peliculas)

@app.route('/admin/peliculas/crear', methods=['GET', 'POST'])
@login_required
def crear_pelicula():
    if request.method == 'POST':
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO peliculas 
            (titulo, descripcion, duracion, clasificacion, anio, director, tagline, puntuacion, imagen_url, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form['titulo'],
            request.form['descripcion'],
            request.form['duracion'],
            request.form['clasificacion'],
            request.form['anio'],
            request.form['director'],
            request.form['tagline'],
            request.form['puntuacion'],
            request.form['imagen_url'],
            'activa'
        ))
        conn.commit()
        return redirect('/admin/peliculas')
    
    return render_template('admin/peliculas_form.html', movie=None)

@app.route('/admin/funciones')
@login_required
def admin_funciones():
    conn = get_db_connection()
    funciones = conn.query("""
        SELECT f.*, p.titulo, COUNT(dt.id) as vendidas
        FROM funciones f
        JOIN peliculas p ON f.pelicula_id = p.id
        LEFT JOIN detalle_tiquete dt ON f.id = dt.funcion_id
        GROUP BY f.id
        ORDER BY f.fecha DESC, f.hora DESC
    """)
    return render_template('admin/funciones_list.html', funciones=funciones)

# ... (más rutas)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## ✅ CHECKLIST IMPLEMENTACIÓN

### Semana 1
- [ ] Crear tabla ADMINS en BD
- [ ] Implementar login/logout
- [ ] Dashboard con estadísticas
- [ ] CRUD películas (Create)
- [ ] CRUD películas (Read, Update, Delete)
- [ ] CRUD funciones (Create, Read, Update, Delete)
- [ ] Reporte ventas con filtros

### Semana 2
- [ ] Dashboard mejorado
- [ ] Gráficos con Chart.js
- [ ] Exportar Excel
- [ ] Visualización de asientos
- [ ] Configuración (precios, contraseña)
- [ ] CSS profesional
- [ ] Testing de toda la app
- [ ] Deployment en producción

---

## 🎨 TIPS DE CSS

```css
/* Sidebar */
.sidebar {
    width: 250px;
    background: #1a1a2e;
    color: white;
    padding: 20px;
    position: fixed;
    height: 100vh;
}

.sidebar a {
    display: block;
    padding: 10px;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    margin: 5px 0;
}

.sidebar a:hover {
    background: #16213e;
}

/* Main content */
.main-content {
    margin-left: 250px;
    padding: 20px;
}

/* Cards */
.card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Botones */
.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
}

.btn-primary {
    background: #00b8d4;
    color: white;
}

.btn-danger {
    background: #e06030;
    color: white;
}
```

---

## 📞 RESUMEN RÁPIDO

| Funcionalidad | Endpoint | Método | Semana |
|---------------|----------|--------|--------|
| Login | /admin/login | GET/POST | 1 |
| Dashboard | /admin/dashboard | GET | 1 |
| Películas CRUD | /admin/peliculas* | GET/POST | 1 |
| Funciones CRUD | /admin/funciones* | GET/POST | 1 |
| Ventas | /admin/ventas | GET | 1 |
| Reportes | /admin/reportes | GET | 2 |
| Asientos | /admin/asientos | GET | 2 |
| Config | /admin/config | GET/POST | 2 |

---
