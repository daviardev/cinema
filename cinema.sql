-- 2. Tabla generos (primero porque es referenciada)
CREATE TABLE generos (
	id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- 3. Tabla peliculas
CREATE TABLE peliculas (
	id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    duracion INT NOT NULL,
    genero_id INT NOT NULL,
    clasificacion VARCHAR(10),
    imagen_url TEXT,
    estado VARCHAR(20) DEFAULT 'activa',
    
    FOREIGN KEY (genero_id) REFERENCES generos(id)
);

-- 4. Tabla funciones
CREATE TABLE funciones (
	id INT AUTO_INCREMENT PRIMARY KEY,
    pelicula_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'disponible',
    
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
);

-- 5. Tabla asientos
CREATE TABLE asientos (
	id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(5) UNIQUE, -- A1, A2...
    fila CHAR(1),
    columna INT
);

-- 6. Tabla tiquetes
CREATE TABLE tiquetes (
	id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    funcion_id INT NOT NULL,
    email VARCHAR(150),
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (funcion_id) REFERENCES funciones(id)
);

-- 7. Tabla detalle_tiquete (🔥 clave para evitar duplicados)
CREATE TABLE detalle_tiquete (
	id INT AUTO_INCREMENT PRIMARY KEY,
    tiquete_id INT NOT NULL,
    asiento_id INT NOT NULL,
    funcion_id INT NOT NULL,
    
    FOREIGN KEY (tiquete_id) REFERENCES tiquetes(id),
    FOREIGN KEY (asiento_id) REFERENCES asientos(id),
    FOREIGN KEY (funcion_id) REFERENCES funciones(id),
    
    UNIQUE (funcion_id, asiento_id)
);

-- 8. Tabla reservas_temporales (opcional pero PRO)
CREATE TABLE reservas_temporales (
	id INT AUTO_INCREMENT PRIMARY KEY,
    funcion_id INT,
    asiento_id INT,
    expiracion TIMESTAMP,
    
    FOREIGN KEY (funcion_id) REFERENCES funciones(id),
    FOREIGN KEY (asiento_id) REFERENCES asientos(id),
    
    UNIQUE (funcion_id, asiento_id)
);

-- 9. Índices para mejorar rendimiento
CREATE INDEX idx_funcion ON detalle_tiquete(funcion_id);
CREATE INDEX idx_asiento ON detalle_tiquete(asiento_id);