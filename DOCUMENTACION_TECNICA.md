# DOCUMENTACIÓN TÉCNICA - SISTEMA DE VENTA DE ENTRADAS CINEVOX

## 1. DESCRIPCIÓN DEL SISTEMA

### 1.1 Objetivo General
Sistema web de venta de entradas de cine que permite a los usuarios:
- Explorar películas disponibles
- Ver funciones/horarios disponibles
- Seleccionar asientos en tiempo real
- Procesar compras
- Recibir entradas por correo electrónico con código QR
- Validar y canjear códigos de entrada
- Consultar historial de compras

### 1.2 Usuarios del Sistema
- **Usuarios Públicos**: Compradores de entradas
- **Administrador**: Gestión de películas, funciones y asientos (no implementado aún)

### 1.3 Características Principales
✅ Catálogo de películas con información detallada (clasificación, duración, sinopsis, actores)
✅ Sistema de selección de asientos con sincronización en tiempo real
✅ Reserva temporal de asientos (15 minutos)
✅ Confirmación de compra con modal detallado
✅ Entrega de entradas por email con código único
✅ Generación de códigos QR para cada entrada
✅ Validación y canje de entradas
✅ Búsqueda y filtrado de películas
✅ Historial de compras (Mis Entradas)
✅ Diseño responsivo (móvil, tablet, escritorio)

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Stack Tecnológico

```
Frontend:
├─ HTML5 (Templates Jinja2)
├─ CSS3 (Responsive Design)
├─ JavaScript Vanilla (SPA - Single Page Application)
└─ Librerías:
   ├─ qrcodejs (Generación de QR)
   └─ jsQR (Lectura de códigos QR)

Backend:
├─ Python 3.9
├─ Flask (Framework Web)
├─ mysql-connector-python (BD)
├─ Flask-Mail (Envío de emails)
└─ Librerías auxiliares:
   ├─ qrcode (Generación de QR en servidor)
   └─ python-dotenv (Gestión de variables de entorno)

Base de Datos:
└─ MySQL 8.4.8
```

### 2.2 Estructura de Carpetas

```
cinema-web/
├── app.py                          # Aplicación principal Flask
├── config.py                       # Configuración
├── db.py                           # Funciones de conexión BD
├── cinema.sql                      # Schema y datos iniciales
├── requirements.txt                # Dependencias Python
├── .env                            # Variables de entorno
├── .gitignore                      # Archivos a ignorar en Git
│
├── static/
│   ├── js/
│   │   └── main.js                # Lógica principal del SPA
│   ├── css/
│   │   └── styles.css             # Estilos de la aplicación
│   └── images/                     # Imágenes (iconos, backgrounds)
│
├── templates/
│   ├── index.html                 # Template principal
│   └── partials/
│       ├── navbar.html            # Navegación
│       ├── viewHome.html          # Vista: Catálogo
│       ├── viewDetails.html       # Vista: Detalle película
│       ├── viewSeats.html         # Vista: Selección asientos
│       ├── viewConfirm.html       # Vista: Confirmación
│       ├── viewValidate.html      # Vista: Validación
│       ├── viewMyTickets.html     # Vista: Mis entradas
│       ├── footer.html            # Pie de página
│       └── modals/
│           ├── emailModal.html    # Modal: Ingresar email
│           └── confirmationModal.html # Modal: Confirmar compra
└── README.md                       # Documentación general
```

### 2.3 Flujo de la Aplicación (SPA)

```
Cliente (Navegador)
    ↓
    [index.html - Template Jinja2]
    ↓
    [main.js - Lógica Frontend]
    ├── Renderiza vistas según estado
    ├── Gestiona interacciones del usuario
    └── Comunica con Backend vía API REST
    ↓
    [app.py - Backend Flask]
    ├── GET /api/peliculas
    ├── GET /api/funciones/{id}
    ├── GET /api/asientos/{id}
    ├── POST /api/procesar-compra
    ├── POST /api/canjear-ticket/{code}
    └── GET /api/mis-tiquetes?email={email}
    ↓
    [db.py - Conexión BD]
    ├── Ejecuta queries
    ├── Gestiona transacciones
    └── Retorna resultados
    ↓
    [MySQL - Base de Datos]
```

### 2.4 Ciclo de Compra

```
1. EXPLORACIÓN
   Usuario → Home (Catálogo) → Busca/Filtra películas

2. SELECCIÓN
   Usuario → Detalle película → Elige función/horario

3. ASIENTOS
   Usuario → Selecciona asientos → Sistema reserva temporalmente (15 min)

4. CONFIRMACIÓN
   Usuario → Modal de confirmación → Revisa total y detalles

5. EMAIL
   Usuario → Ingresa email → Sistema envía entrada + QR

6. VALIDACIÓN
   Usuario → Código en entrada → Lee QR o ingresa código manualmente

7. CANJE
   Usuario → Presenta entrada → Sistema marca como canjeada
```

---

## 3. MODELO DE BASE DE DATOS

### 3.1 Diagrama ER (Relaciones)

```
┌──────────────────┐
│   PELICULAS      │
├──────────────────┤
│ id (PK)          │
│ titulo           │
│ descripcion      │
│ duracion         │
│ clasificacion    │
│ imagen_url       │
│ estado           │
│ puntuacion       │
│ anio             │
│ tagline          │
│ director         │
└──────┬───────────┘
       │ 1:N
       │
    ┌──┴─────────────────────────┐
    │                            │
    │                    ┌───────▼────────┐
    │                    │  FUNCIONES     │
    │                    ├────────────────┤
    │                    │ id (PK)        │
    │                    │ pelicula_id(FK)│
    │                    │ fecha          │
    │                    │ hora           │
    │                    │ precio         │
    │                    │ estado         │
    │                    │ sala           │
    │                    │ tecnologia     │
    │                    └────┬──────────┬┘
    │                         │ 1:N   1:N
    │         ┌───────────────┘         │
    │         │                         │
    │    ┌────▼──────────┐      ┌──────▼─────────────┐
    │    │   ASIENTOS   │      │ RESERVAS_TEMPORALES│
    │    ├──────────────┤      ├────────────────────┤
    │    │ id (PK)      │      │ id (PK)            │
    │    │ numero (UK)  │      │ funcion_id (FK)    │
    │    │ fila         │      │ asiento_id (FK)    │
    │    │ columna      │      │ expiracion         │
    │    │ tipo_id (FK) │      └────────┬───────────┘
    │    └────┬─────────┘               │
    │         │                         │
    │    ┌────▼──────────────┐          │
    │    │  TIPOS_ASIENTOS   │          │
    │    ├───────────────────┤          │
    │    │ id (PK)           │          │
    │    │ nombre            │          │
    │    │ precio            │          │
    │    └───────────────────┘          │
    │                                   │
    │ ┌───────────────────────────────┐ │
    │ │     DETALLE_TIQUETE (Join)    │◄┘
    │ ├───────────────────────────────┤
    │ │ id (PK)                       │
    │ │ tiquete_id (FK)               │
    │ │ asiento_id (FK)               │
    │ │ funcion_id (FK)               │
    │ └───────────────────────────────┘
    │
    │ ┌─────────────────────────────┐
    │ │  PELICULA_ACTORES (Join)    │
    │ ├─────────────────────────────┤
    │ │ pelicula_id (FK)            │
    │ │ actor_id (FK)               │
    │ └─────────────────────────────┘
    │
    │ ┌─────────────────────────────┐
    │ │ PELICULA_GENEROS (Join)     │
    │ ├─────────────────────────────┤
    │ │ pelicula_id (FK)            │
    │ │ genero_id (FK)              │
    │ └─────────────────────────────┘
    │
    └──────▶┌──────────────┐   ┌──────────┐
            │  TIQUETES    │   │  ACTORES │
            ├──────────────┤   ├──────────┤
            │ id (PK)      │   │ id (PK)  │
            │ codigo (UK)  │   │ nombre   │
            │ funcion_id   │   └──────────┘
            │ email        │
            │ total        │   ┌──────────┐
            │ estado       │   │  GENEROS │
            │ fecha_compra │   ├──────────┤
            └──────────────┘   │ id (PK)  │
                               │ nombre   │
                               └──────────┘
```

### 3.2 Descripción de Tablas

#### PELICULAS
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | Identificador único |
| titulo | VARCHAR(100) | Nombre de la película |
| descripcion | TEXT | Sinopsis completa |
| duracion | INT | Duración en minutos |
| clasificacion | VARCHAR(10) | Restricción de edad (PG-13, R, etc) |
| imagen_url | TEXT | URL de póster |
| estado | VARCHAR(20) | 'activa', 'proxima', 'finalizada' |
| puntuacion | DECIMAL(3,1) | Calificación 0-10 |
| anio | INT | Año de estreno |
| tagline | VARCHAR(255) | Frase promocional |
| director | VARCHAR(100) | Nombre del director |

#### FUNCIONES
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | Identificador único |
| pelicula_id | INT (FK) | Referencia a película |
| fecha | DATE | Fecha de función |
| hora | TIME | Hora de función |
| precio | DECIMAL(10,2) | Precio base de entrada |
| estado | VARCHAR(20) | 'disponible', 'completa', 'cancelada' |
| sala | VARCHAR(50) | Número/nombre de sala |
| tecnologia | VARCHAR(50) | Formato (2D, IMAX, Dolby) |

#### ASIENTOS
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | Identificador único |
| numero | VARCHAR(5) (UK) | Código de asiento (A1, B15, etc) |
| fila | CHAR(1) | Fila (A-J) |
| columna | INT | Columna (1-18) |
| tipo_id | BIGINT (FK) | Referencia a tipo de asiento |

#### TIPOS_ASIENTOS
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT (PK) | Identificador único |
| nombre | VARCHAR(20) | 'estandard', 'premium', 'vip' |
| precio | DECIMAL(5,2) | Precio adicional |

#### TIQUETES
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | Identificador único |
| codigo | VARCHAR(50) (UK) | Código único (TKT-XXXX-XXXXX) |
| funcion_id | INT (FK) | Referencia a función |
| email | VARCHAR(150) | Email del comprador |
| total | DECIMAL(10,2) | Total pagado |
| estado | VARCHAR(20) | 'activo', 'canjeado', 'expirado' |
| fecha_compra | TIMESTAMP | Fecha/hora de compra |

#### DETALLE_TIQUETE
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | Identificador único |
| tiquete_id | INT (FK) | Referencia a tiquete |
| asiento_id | INT (FK) | Referencia a asiento |
| funcion_id | INT (FK) | Referencia a función |

#### RESERVAS_TEMPORALES
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT (PK) | Identificador único |
| funcion_id | INT (FK) | Referencia a función |
| asiento_id | INT (FK) | Referencia a asiento |
| expiracion | TIMESTAMP | Fecha/hora de expiración (15 min) |

#### ACTORES, PELICULA_ACTORES, GENEROS, PELICULA_GENEROS
Tablas de relación N:N para películas con múltiples actores y géneros.

### 3.3 Estados de Asientos

```
DISPONIBLE   → No tiene reserva temporal ni compra
RESERVADO    → Tiene reserva temporal activa (15 min)
OCUPADO      → Ya fue comprado/canjeado
MANTENIMIENTO → Fuera de servicio
```

---

## 4. ENDPOINTS DEL API

### 4.1 URL Base
```
Desarrollo: http://localhost:5000
Producción: https://[dominio].com
```

### 4.2 Endpoints Disponibles

#### 1. **GET /api/peliculas**
Obtiene el listado completo de películas disponibles.

**Request:**
```
GET /api/peliculas
```

**Response (200):**
```json
[
  {
    "id": 1,
    "titulo": "Spider-Man: Brand New Day",
    "descripcion": "presenta a un Peter Parker...",
    "duracion": 180,
    "clasificacion": "PG-13",
    "imagen_url": "https://...",
    "estado": "Estreno",
    "puntuacion": 4.5,
    "anio": 2026,
    "tagline": "Un gran poder, conlleva...",
    "director": "Destin Daniel Cretton",
    "categorias": "Acción · Ciencia Ficción",
    "actores": "Tom Holland · Zendaya · ..."
  }
]
```

---

#### 2. **GET /api/funciones/{pelicula_id}**
Obtiene todas las funciones de una película específica.

**Request:**
```
GET /api/funciones/1
```

**Response (200):**
```json
[
  {
    "id": 1,
    "pelicula_id": 1,
    "fecha": "2026-03-31",
    "hora": "14:30:00",
    "precio": 18.50,
    "estado": "disponible",
    "sala": "Sala IMAX",
    "tecnologia": "IMAX 4K"
  },
  {
    "id": 2,
    "pelicula_id": 1,
    "fecha": "2026-03-31",
    "hora": "17:15:00",
    "precio": 15.00,
    "estado": "disponible",
    "sala": "Sala Premium",
    "tecnologia": "Dolby Vision"
  }
]
```

---

#### 3. **GET /api/asientos/{funcion_id}**
Obtiene los asientos de una función con su estado actual.

**Request:**
```
GET /api/asientos/1
```

**Response (200):**
```json
[
  {
    "id": 1,
    "numero": "A1",
    "fila": "A",
    "columna": 1,
    "tipo": "estandard",
    "precio": 12.50,
    "estado": "disponible"
  },
  {
    "id": 2,
    "numero": "A2",
    "fila": "A",
    "columna": 2,
    "tipo": "estandard",
    "precio": 12.50,
    "estado": "reservado"
  },
  {
    "id": 15,
    "numero": "C5",
    "fila": "C",
    "columna": 5,
    "tipo": "vip",
    "precio": 18.50,
    "estado": "ocupado"
  }
]
```

**Estados posibles:**
- `disponible`: Puede ser comprado
- `reservado`: Reserva temporal activa (15 min)
- `ocupado`: Ya fue comprado

---

#### 4. **POST /api/procesar-compra**
Procesa la compra de entradas y envía email con QR.

**Request:**
```
POST /api/procesar-compra
Content-Type: application/json

{
  "funcion_id": 1,
  "asientos_ids": [1, 2, 3],
  "email": "usuario@example.com",
  "total": 37.50
}
```

**Response (200) - Éxito:**
```json
{
  "success": true,
  "ticket_code": "TKT-4890-YZM30",
  "message": "Compra procesada. Revisa tu email.",
  "total": 37.50
}
```

**Response (400) - Error:**
```json
{
  "error": "Algún asiento ya no está disponible"
}
```

**Proceso interno:**
1. Valida que asientos estén disponibles
2. Crea registro en tabla TIQUETES
3. Crea detalles en DETALLE_TIQUETE
4. Genera código QR único
5. Envía email con QR y código
6. Retorna código de éxito

---

#### 5. **GET /api/verificar-ticket/{codigo}**
Verifica si un código de entrada es válido sin canjearlo.

**Request:**
```
GET /api/verificar-ticket/TKT-4890-YZM30
```

**Response (200) - Válido:**
```json
{
  "valido": true,
  "codigo": "TKT-4890-YZM30",
  "pelicula": "Spider-Man: Brand New Day",
  "funcion": "2026-04-02 15:00",
  "sala": "Sala Premium",
  "asientos": ["C5", "C6", "C7"],
  "estado": "activo"
}
```

**Response (404) - Inválido:**
```json
{
  "error": "Código no encontrado o ya fue canjeado"
}
```

---

#### 6. **POST /api/canjear-ticket/{codigo}**
Marca un ticket como canjeado (usado en entrada del cine).

**Request:**
```
POST /api/canjear-ticket/TKT-4890-YZM30
```

**Response (200) - Éxito:**
```json
{
  "success": true,
  "message": "Entrada canjeada exitosamente",
  "ticket": {
    "codigo": "TKT-4890-YZM30",
    "pelicula": "Spider-Man: Brand New Day",
    "asientos": ["C5", "C6", "C7"]
  }
}
```

**Response (400) - Error:**
```json
{
  "error": "Esta entrada ya fue canjeada"
}
```

---

#### 7. **GET /api/mis-tiquetes?email={email}**
Obtiene el historial de compras de un usuario por email.

**Request:**
```
GET /api/mis-tiquetes?email=usuario@example.com
```

**Response (200):**
```json
[
  {
    "id": 1,
    "codigo": "TKT-4890-YZM30",
    "pelicula": "Spider-Man: Brand New Day",
    "fecha": "2026-04-02",
    "hora": "15:00",
    "sala": "Sala Premium",
    "asientos": "C5, C6, C7",
    "total": 46.00,
    "estado": "activo",
    "fecha_compra": "2026-04-01 19:30:13"
  },
  {
    "id": 2,
    "codigo": "TKT-9128-WQW48",
    "pelicula": "Spider-Man: Brand New Day",
    "fecha": "2026-03-31",
    "hora": "17:15",
    "sala": "Sala Premium",
    "asientos": "A4",
    "total": 12.50,
    "estado": "canjeado",
    "fecha_compra": "2026-04-01 20:14:42"
  }
]
```

**Ordenamiento:** Por fecha de compra, más recientes primero.

---

### 4.3 Códigos de Respuesta HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK - Solicitud exitosa |
| 400 | Bad Request - Parámetros inválidos |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## 5. FLUJO DE DATOS DETALLADO

### 5.1 Compra de Entrada

```
Usuario selecciona asientos
    ↓
[Frontend: reserva temporal en localStorage]
    ↓
Usuario hace click en "Comprar"
    ↓
[Modal: Solicita email]
    ↓
POST /api/procesar-compra
    {funcion_id, asientos_ids, email, total}
    ↓
[Backend: app.py → procesar_compra()]
    ├─ Valida asientos disponibles en BD
    ├─ Crea TIQUETE con código único (TKT-XXXX-XXXXX)
    ├─ Crea registros en DETALLE_TIQUETE
    ├─ Borra RESERVAS_TEMPORALES
    ├─ Genera imagen QR con código
    └─ Envía email con:
        - Código de entrada
        - Detalles de película/función
        - Imagen del QR
    ↓
[Frontend: Muestra mensaje de éxito]
    ↓
Usuario recibe email con entrada + QR
```

### 5.2 Validación en Caja (Entrada del Cine)

```
Usuario presenta entrada o código
    ↓
[Acomodador/Vendedor escanea QR O]
[Ingresa código manualmente en app]
    ↓
GET /api/verificar-ticket/{codigo}
    ↓
[Backend: Valida código en BD]
    ├─ Busca en tabla TIQUETES
    ├─ Si existe y estado = 'activo'
    └─ Retorna detalles
    ↓
[Si válido: POST /api/canjear-ticket/{codigo}]
    ├─ Actualiza estado a 'canjeado'
    └─ Registra fecha/hora de canje
    ↓
✅ Entrada validada - Puede entrar
```

---

## 6. SEGURIDAD

### 6.1 Medidas Implementadas
- Variables sensibles en `.env` (no en código)
- Códigos de entrada únicos de 16 caracteres
- Validación de email antes de comprar
- Transacciones de BD para garantizar consistencia
- CORS deshabilitado (solo requests locales)

### 6.2 Recomendaciones para Producción
- [ ] Implementar autenticación de usuarios (JWT)
- [ ] Validación de pagos reales (MercadoPago, Stripe)
- [ ] Rate limiting en endpoints
- [ ] Encriptación de datos sensibles
- [ ] HTTPS obligatorio
- [ ] Tokens de sesión seguros

---

## 7. DESPLIEGUE

### 7.1 Variables de Entorno (.env)
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=xxx
DB_NAME=cinema

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu@gmail.com
MAIL_PASSWORD=app_password
EMAIL_DEFAULT_SENDER=tu@gmail.com

FLASK_ENV=production
FLASK_DEBUG=False
```

### 7.2 Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 7.3 Ejecutar Localmente
```bash
python app.py
```

Accede a: `http://localhost:5000`

### 7.4 Deploy en Render
1. Crear repositorio en GitHub
2. Conectar Render a GitHub
3. Configurar variables de entorno en Render
4. Render ejecuta automáticamente `pip install -r requirements.txt`
5. Render inicia con `gunicorn app:app`

---

## 8. ESTADÍSTICAS DEL SISTEMA

- **Películas**: 1 (Spider-Man: Brand New Day)
- **Funciones**: 10 disponibles
- **Asientos totales**: 180 (10 filas × 18 columnas)
  - 36 Estándar @ $12.50
  - 90 Premium @ $15.00
  - 54 VIP @ $18.50
- **Tiempo reserva temporal**: 15 minutos
- **Formato códigos**: TKT-XXXX-XXXXX (16 caracteres)

---

## 9. NOTAS TÉCNICAS ADICIONALES

### 9.1 Sincronización en Tiempo Real
El frontend hace polling cada **1.2 segundos** para verificar cambios en asientos:
```javascript
setInterval(pollSeatUpdates, 1200);
```

Esto garantiza que múltiples usuarios vean cambios casi en tiempo real.

### 9.2 Expiración de Reservas
Las reservas temporales expiran automáticamente después de 15 minutos. Para limpiar:
```sql
DELETE FROM reservas_temporales 
WHERE expiracion < NOW();
```

### 9.3 Generación de Códigos QR
El sistema genera dos tipos de QR:
- **Frontend**: Mostrar en modal (qrcodejs)
- **Email**: Incluir en el body del email (qrcode library python)

---

**Última actualización**: 5 de abril de 2026
**Versión**: 1.0
**Autor**: Equipo de Desarrollo
