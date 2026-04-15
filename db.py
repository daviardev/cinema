import mysql.connector
import bcrypt

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def get_peliculas_cartelera():
    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            p.id,
            p.titulo,
            p.duracion,
            p.clasificacion,
            p.imagen_url,
            p.estado,
            p.anio,
            p.director,
            p.puntuacion,
            p.descripcion,
            GROUP_CONCAT(DISTINCT g.nombre ORDER BY g.nombre SEPARATOR ' · ') AS categorias,
            GROUP_CONCAT(DISTINCT a.nombre ORDER BY a.nombre SEPARATOR ' · ') AS actores
        FROM peliculas p
        LEFT JOIN pelicula_generos pg ON p.id = pg.pelicula_id
        LEFT JOIN generos g ON pg.genero_id = g.id
        LEFT JOIN pelicula_actores pa ON p.id = pa.pelicula_id
        LEFT JOIN actores a ON pa.actor_id = a.id
        GROUP BY p.id
    """

    cursor.execute(query)

    peliculas = cursor.fetchall()

    cursor.close()
    conn.close()
    return peliculas

def get_funciones_por_pelicula(pelicula_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            f.id,
            f.pelicula_id,
            f.fecha,
            f.hora,
            f.precio,
            f.estado,
            f.sala,
            f.tecnologia
        FROM funciones f
        WHERE f.pelicula_id = %s
        ORDER BY f.fecha, f.hora
    """

    cursor.execute(query, (pelicula_id,))
    funciones = cursor.fetchall()

    # Convertir tipos no serializables a JSON
    for f in funciones:
        f['fecha'] = str(f['fecha']) if f['fecha'] else None
        f['hora'] = str(f['hora']) if f['hora'] else None
        f['precio'] = float(f['precio']) if f['precio'] else None

    cursor.close()
    conn.close()
    return funciones

def get_asientos_disponibles(funcion_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            a.id,
            a.numero,
            a.fila,
            a.columna,
            ta.nombre AS tipo,
            ta.precio,
            CASE
                WHEN dt.id IS NOT NULL THEN 'ocupado'
                WHEN rt.id IS NOT NULL THEN 'reservado'
                ELSE 'disponible'
            END AS estado
        FROM asientos a
        LEFT JOIN tipos_asientos ta ON a.tipo_id = ta.id
        LEFT JOIN detalle_tiquete dt ON a.id = dt.asiento_id AND dt.funcion_id = %s
        LEFT JOIN reservas_temporales rt ON a.id = rt.asiento_id AND rt.funcion_id = %s
        ORDER BY a.fila, a.columna
    """

    cursor.execute(query, (funcion_id, funcion_id))
    asientos = cursor.fetchall()

    # Convertir tipos no serializables a JSON
    for a in asientos:
        a['precio'] = float(a['precio']) if a['precio'] else None

    cursor.close()
    conn.close()
    return asientos

def create_reserva_temporal(funcion_id, asiento_id, minutos_expiracion=15):
    """
    Crear una reserva temporal para un asiento.
    La reserva expira después de minutos_expiracion minutos.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO reservas_temporales (funcion_id, asiento_id, expiracion)
        VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL %s MINUTE))
        ON DUPLICATE KEY UPDATE expiracion = DATE_ADD(NOW(), INTERVAL %s MINUTE)
    """

    try:
        cursor.execute(query, (funcion_id, asiento_id, minutos_expiracion, minutos_expiracion))
        conn.commit()
        result = True
    except Exception as e:
        print(f"Error creating reserva_temporal: {e}")
        result = False
    finally:
        cursor.close()
        conn.close()

    return result

def delete_reserva_temporal(funcion_id, asiento_id):
    """
    Eliminar una reserva temporal.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM reservas_temporales WHERE funcion_id = %s AND asiento_id = %s"

    try:
        cursor.execute(query, (funcion_id, asiento_id))
        conn.commit()
        result = True
    except Exception as e:
        print(f"Error deleting reserva_temporal: {e}")
        result = False
    finally:
        cursor.close()
        conn.close()

    return result

def process_purchase(funcion_id, asiento_ids, email, ticket_code, total=0):
    """
    Procesar la compra: crear tiquete y detalle_tiquete.
    Retorna el ticket_id si es exitoso, None si falla.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print(f"Processing purchase: funcion_id={funcion_id}, asientos={asiento_ids}, email={email}, code={ticket_code}, total={total}")
        
        # 1. Insertar en tiquetes
        insert_ticket = """
            INSERT INTO tiquetes (codigo, funcion_id, email, total, estado)
            VALUES (%s, %s, %s, %s, 'activo')
        """
        cursor.execute(insert_ticket, (ticket_code, funcion_id, email, total))
        conn.commit()
        print(f"Ticket inserted with ID: {cursor.lastrowid}")
        
        # Obtener el ID del tiquete insertado
        ticket_id = cursor.lastrowid
        
        # 2. Insertar en detalle_tiquete para cada asiento
        insert_detail = """
            INSERT INTO detalle_tiquete (tiquete_id, asiento_id, funcion_id)
            VALUES (%s, %s, %s)
        """
        for asiento_id in asiento_ids:
            print(f"Inserting detail: ticket={ticket_id}, asiento={asiento_id}, funcion={funcion_id}")
            cursor.execute(insert_detail, (ticket_id, asiento_id, funcion_id))
        
        conn.commit()
        print(f"All details inserted successfully")
        
        # 3. Limpiar reservas temporales
        for asiento_id in asiento_ids:
            delete_query = "DELETE FROM reservas_temporales WHERE funcion_id = %s AND asiento_id = %s"
            cursor.execute(delete_query, (funcion_id, asiento_id))
            print(f"Temporary reservation cleaned for asiento {asiento_id}")
        
        conn.commit()
        print(f"Purchase processed successfully. Ticket ID: {ticket_id}")
        return ticket_id
        
    except Exception as e:
        print(f"Error processing purchase: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_ticket_by_code(codigo):
    """Obtener detalles completos de un ticket por código"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            t.id,
            t.codigo,
            t.email,
            t.total,
            t.estado,
            t.fecha_compra,
            f.fecha,
            f.hora,
            f.sala,
            f.tecnologia,
            p.titulo as pelicula_titulo,
            GROUP_CONCAT(CONCAT(a.fila, a.columna) ORDER BY a.fila, a.columna SEPARATOR ', ') AS asientos
        FROM tiquetes t
        JOIN funciones f ON t.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        LEFT JOIN detalle_tiquete dt ON t.id = dt.tiquete_id
        LEFT JOIN asientos a ON dt.asiento_id = a.id
        WHERE t.codigo = %s
        GROUP BY t.id
    """
    
    cursor.execute(query, (codigo,))
    ticket = cursor.fetchone()
    
    if ticket:
        # Convertir tipos no serializables
        if ticket.get('fecha'):
            ticket['fecha'] = str(ticket['fecha'])
        if ticket.get('hora'):
            ticket['hora'] = str(ticket['hora'])
        if ticket.get('total'):
            ticket['total'] = float(ticket['total'])
        if ticket.get('fecha_compra'):
            ticket['fecha_compra'] = str(ticket['fecha_compra'])
        
        # Enriquecer con datos de asientos
        set_asientos = set()
        inner_query = """
            SELECT DISTINCT a.numero, a.id
            FROM detalle_tiquete dt
            JOIN asientos a ON dt.asiento_id = a.id
            WHERE dt.tiquete_id = %s
        """
        inner_cursor = conn.cursor(dictionary=True)
        inner_cursor.execute(inner_query, (ticket['id'],))
        asientos_info = inner_cursor.fetchall()
        inner_cursor.close()
        
        ticket['asientos'] = asientos_info if asientos_info else []
    
    cursor.close()
    conn.close()
    return ticket

def mark_ticket_used(codigo):
    """Marcar un ticket como canjeado"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "UPDATE tiquetes SET estado = 'canjeado' WHERE codigo = %s AND estado = 'activo'"
    
    try:
        cursor.execute(query, (codigo,))
        conn.commit()
        result = cursor.rowcount > 0
    except Exception as e:
        print(f"Error marking ticket as used: {e}")
        result = False
    finally:
        cursor.close()
        conn.close()
    
    return result

def get_funcion_with_details(funcion_id):
    """
    Obtener una función con detalles de la película y otros datos.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            f.id,
            f.pelicula_id,
            f.fecha,
            f.hora,
            f.precio,
            f.estado,
            f.sala,
            f.tecnologia,
            p.titulo AS pelicula
        FROM funciones f
        LEFT JOIN peliculas p ON f.pelicula_id = p.id
        WHERE f.id = %s
    """

    cursor.execute(query, (funcion_id,))
    funcion = cursor.fetchone()

    if funcion:
        funcion['fecha'] = str(funcion['fecha']) if funcion['fecha'] else None
        funcion['hora'] = str(funcion['hora']) if funcion['hora'] else None
        funcion['precio'] = float(funcion['precio']) if funcion['precio'] else None

    cursor.close()
    conn.close()
    return funcion


def send_ticket_email(email, codigo, pelicula_titulo, funcion_data, asientos_list, mail):
    """Enviar ticket por email"""
    from flask_mail import Message
    
    # Extract seat numbers from list of dicts
    if asientos_list and isinstance(asientos_list, list):
        asientos_str = ', '.join([str(a.get('numero', a.get('id', ''))) for a in asientos_list if isinstance(a, dict)])
    else:
        asientos_str = 'N/A'
    fecha = funcion_data.get('fecha', 'N/A')
    hora = funcion_data.get('hora', 'N/A')
    sala = funcion_data.get('sala', 'N/A')
    tecnologia = funcion_data.get('tecnologia', 'N/A')
    total = funcion_data.get('total', 0)
    
    html_body = f"""
    <html style="font-family: Arial; background: #1a1a1a; color: #fff;">
        <body style="padding: 20px; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background: #222; padding: 30px; border-radius: 10px; border: 2px solid #9580e0;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #9580e0; margin: 0;">🎬 Tu Entrada está Lista</h1>
                </div>
                
                <div style="background: #111; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 10px 0;"><strong>📽️ Película:</strong> {pelicula_titulo}</p>
                    <p style="margin: 10px 0;"><strong>📅 Fecha:</strong> {fecha}</p>
                    <p style="margin: 10px 0;"><strong>🕐 Hora:</strong> {hora}</p>
                    <p style="margin: 10px 0;"><strong>🎪 Sala:</strong> {sala}</p>
                    <p style="margin: 10px 0;"><strong>🎥 Formato:</strong> {tecnologia}</p>
                    <p style="margin: 10px 0;"><strong>💺 Asientos:</strong> {asientos_str}</p>
                    <p style="margin: 10px 0;"><strong>💵 Total:</strong> ${total:.2f}</p>
                </div>
                
                <div style="background: #9580e0; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
                    <p style="font-size: 12px; color: #000; margin: 0 0 10px 0;">TU CÓDIGO DE ENTRADA</p>
                    <p style="font-size: 32px; font-weight: bold; color: #000; letter-spacing: 2px; margin: 0;">
                        {codigo}
                    </p>
                    <div style="margin-top: 15px;">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={codigo}" alt="QR Code" style="width: 150px; height: 150px; border-radius: 4px; background: white; padding: 8px;" />
                    </div>
                </div>
                
                <div style="background: #111; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #aaa; font-size: 14px;">
                        <strong>Instrucciones:</strong><br><br>
                        1. Escanea el código QR en la entrada con tu dispositivo<br>
                        2. O presenta el código: {codigo}<br>
                        3. Disfruta de la película 🍿
                    </p>
                </div>
                
                <hr style="border: none; border-top: 1px solid #444; margin: 30px 0;">
                <p style="color: #666; font-size: 12px; text-align: center; margin: 0;">
                    CineVOX © 2026 | No responder a este email
                </p>
            </div>
        </body>
    </html>
    """
    
    try:
        msg = Message(
            subject=f'Tu Entrada: {codigo} - {pelicula_titulo}',
            recipients=[email],
            html=html_body
        )
        mail.send(msg)
        print(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# ==========================================
# FUNCIONES PARA DASHBOARD ADMINISTRATIVO
# ==========================================

def get_dashboard_stats():
    """Obtener estadísticas para el dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    stats = {}
    
    # Total películas
    cursor.execute("SELECT COUNT(*) as total FROM peliculas")
    stats['total_peliculas'] = cursor.fetchone()['total']
    
    # Total funciones
    cursor.execute("SELECT COUNT(*) as total FROM funciones")
    stats['total_funciones'] = cursor.fetchone()['total']
    
    # Total tickets vendidos
    cursor.execute("SELECT COUNT(*) as total FROM tiquetes WHERE estado = 'activo'")
    stats['total_tickets'] = cursor.fetchone()['total']
    
    # Ingresos totales
    cursor.execute("SELECT SUM(total) as total FROM tiquetes WHERE estado = 'activo'")
    result = cursor.fetchone()
    stats['total_ingresos'] = float(result['total'] or 0)
    
    # Tickets canjeados hoy
    cursor.execute("""
        SELECT COUNT(*) as total 
        FROM tiquetes 
        WHERE estado = 'canjeado' 
        AND DATE(fecha_compra) = CURDATE()
    """)
    stats['tickets_canjeados_hoy'] = cursor.fetchone()['total']
    
    cursor.close()
    conn.close()
    return stats

def get_all_peliculas():
    """Obtener todas las películas con detalles completos"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            p.*,
            GROUP_CONCAT(DISTINCT g.nombre ORDER BY g.nombre SEPARATOR ', ') AS generos,
            GROUP_CONCAT(DISTINCT a.nombre ORDER BY a.nombre SEPARATOR ', ') AS actores
        FROM peliculas p
        LEFT JOIN pelicula_generos pg ON p.id = pg.pelicula_id
        LEFT JOIN generos g ON pg.genero_id = g.id
        LEFT JOIN pelicula_actores pa ON p.id = pa.pelicula_id
        LEFT JOIN actores a ON pa.actor_id = a.id
        GROUP BY p.id
        ORDER BY p.id DESC
    """
    
    cursor.execute(query)
    peliculas = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return peliculas

def get_pelicula_by_id(pelicula_id):
    """Obtener una película por ID con sus géneros y actores"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Obtener película
    cursor.execute("SELECT * FROM peliculas WHERE id = %s", (pelicula_id,))
    pelicula = cursor.fetchone()
    
    if pelicula:
        # Obtener géneros
        cursor.execute("""
            SELECT g.id, g.nombre 
            FROM generos g 
            JOIN pelicula_generos pg ON g.id = pg.genero_id 
            WHERE pg.pelicula_id = %s
        """, (pelicula_id,))
        pelicula['generos'] = cursor.fetchall()
        
        # Obtener actores
        cursor.execute("""
            SELECT a.id, a.nombre 
            FROM actores a 
            JOIN pelicula_actores pa ON a.id = pa.actor_id 
            WHERE pa.pelicula_id = %s
        """, (pelicula_id,))
        pelicula['actores'] = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return pelicula

def create_pelicula(titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion, generos=None, actores=None):
    """Crear una nueva película"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO peliculas (titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'activa')
        """, (titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion))
        
        pelicula_id = cursor.lastrowid
        
        # Agregar géneros
        if generos:
            for genero_id in generos:
                cursor.execute("INSERT INTO pelicula_generos (pelicula_id, genero_id) VALUES (%s, %s)", (pelicula_id, genero_id))
        
        # Agregar actores
        if actores:
            for actor_id in actores:
                cursor.execute("INSERT INTO pelicula_actores (pelicula_id, actor_id) VALUES (%s, %s)", (pelicula_id, actor_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_pelicula(pelicula_id, titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion, generos=None, actores=None):
    """Actualizar una película"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE peliculas 
            SET titulo=%s, descripcion=%s, duracion=%s, clasificacion=%s, imagen_url=%s, 
                anio=%s, director=%s, puntuacion=%s
            WHERE id=%s
        """, (titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion, pelicula_id))
        
        # Eliminar géneros existentes
        cursor.execute("DELETE FROM pelicula_generos WHERE pelicula_id = %s", (pelicula_id,))
        
        # Agregar géneros nuevos
        if generos:
            for genero_id in generos:
                cursor.execute("INSERT INTO pelicula_generos (pelicula_id, genero_id) VALUES (%s, %s)", (pelicula_id, genero_id))
        
        # Eliminar actores existentes
        cursor.execute("DELETE FROM pelicula_actores WHERE pelicula_id = %s", (pelicula_id,))
        
        # Agregar actores nuevos
        if actores:
            for actor_id in actores:
                cursor.execute("INSERT INTO pelicula_actores (pelicula_id, actor_id) VALUES (%s, %s)", (pelicula_id, actor_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_pelicula(pelicula_id):
    """Eliminar una película"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Eliminar relaciones primero
        cursor.execute("DELETE FROM pelicula_generos WHERE pelicula_id = %s", (pelicula_id,))
        cursor.execute("DELETE FROM pelicula_actores WHERE pelicula_id = %s", (pelicula_id,))
        cursor.execute("DELETE FROM funciones WHERE pelicula_id = %s", (pelicula_id,))
        
        # Eliminar película
        cursor.execute("DELETE FROM peliculas WHERE id = %s", (pelicula_id,))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_funciones():
    """Obtener todas las funciones con detalles"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT f.*, p.titulo as pelicula_titulo
        FROM funciones f
        JOIN peliculas p ON f.pelicula_id = p.id
        ORDER BY f.fecha DESC, f.hora DESC
    """
    
    cursor.execute(query)
    funciones = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return funciones

def get_funcion_by_id(funcion_id):
    """Obtener una función por ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT f.*, p.titulo as pelicula_titulo
        FROM funciones f
        JOIN peliculas p ON f.pelicula_id = p.id
        WHERE f.id = %s
    """, (funcion_id,))
    
    funcion = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return funcion

def create_funcion(pelicula_id, fecha, hora, precio, sala, tecnologia):
    """Crear una nueva función validando conflictos de horarios"""
    from datetime import datetime, timedelta
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Obtener duración de la película
        cursor.execute("SELECT duracion FROM peliculas WHERE id = %s", (pelicula_id,))
        pelicula = cursor.fetchone()
        if not pelicula:
            raise ValueError(f"Película con ID {pelicula_id} no encontrada")
        
        duracion_minutos = pelicula['duracion']
        
        # 2. Convertir hora a datetime y calcular hora_fin
        hora_obj = datetime.strptime(hora, '%H:%M').time()
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_inicio = datetime.combine(fecha_obj, hora_obj)
        hora_fin_obj = hora_inicio + timedelta(minutes=duracion_minutos)
        hora_fin = hora_fin_obj.time()
        
        # 3. Validar que no haya conflicto en la misma sala
        cursor.execute("""
            SELECT id, hora, hora_fin
            FROM funciones
            WHERE sala = %s AND fecha = %s
        """, (sala, fecha))
        
        funciones_existentes = cursor.fetchall()
        
        for funcion in funciones_existentes:
            h_inicio_existente = datetime.combine(fecha_obj, funcion['hora'])
            h_fin_existente = datetime.combine(fecha_obj, funcion['hora_fin'])
            
            # Verificar solapamiento
            if (hora_inicio < h_fin_existente and hora_fin_obj > h_inicio_existente):
                raise ValueError(
                    f"Conflicto de horarios en {sala}: "
                    f"Hay una función de {funcion['hora']} a {funcion['hora_fin']}"
                )
        
        # 4. Insertar función con hora_fin calculada
        cursor.execute("""
            INSERT INTO funciones (pelicula_id, fecha, hora, hora_fin, precio, sala, tecnologia, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'disponible')
        """, (pelicula_id, fecha, hora, hora_fin.strftime('%H:%M:%S'), precio, sala, tecnologia))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_funcion(funcion_id, pelicula_id, fecha, hora, precio, sala, tecnologia):
    """Actualizar una función validando conflictos de horarios"""
    from datetime import datetime, timedelta
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. Obtener duración de la película
        cursor.execute("SELECT duracion FROM peliculas WHERE id = %s", (pelicula_id,))
        pelicula = cursor.fetchone()
        if not pelicula:
            raise ValueError(f"Película con ID {pelicula_id} no encontrada")
        
        duracion_minutos = pelicula['duracion']
        
        # 2. Convertir hora a datetime y calcular hora_fin
        hora_obj = datetime.strptime(hora, '%H:%M').time()
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_inicio = datetime.combine(fecha_obj, hora_obj)
        hora_fin_obj = hora_inicio + timedelta(minutes=duracion_minutos)
        hora_fin = hora_fin_obj.time()
        
        # 3. Validar que no haya conflicto en la misma sala
        cursor.execute("""
            SELECT id, hora, hora_fin
            FROM funciones
            WHERE sala = %s AND fecha = %s AND id != %s
        """, (sala, fecha, funcion_id))
        
        funciones_existentes = cursor.fetchall()
        
        for funcion in funciones_existentes:
            h_inicio_existente = datetime.combine(fecha_obj, funcion['hora'])
            h_fin_existente = datetime.combine(fecha_obj, funcion['hora_fin'])
            
            # Verificar solapamiento
            if (hora_inicio < h_fin_existente and hora_fin_obj > h_inicio_existente):
                raise ValueError(
                    f"Conflicto de horarios en {sala}: "
                    f"Hay una función de {funcion['hora']} a {funcion['hora_fin']}"
                )
        
        # 4. Actualizar función con hora_fin calculada
        cursor.execute("""
            UPDATE funciones 
            SET pelicula_id=%s, fecha=%s, hora=%s, hora_fin=%s, precio=%s, sala=%s, tecnologia=%s
            WHERE id=%s
        """, (pelicula_id, fecha, hora, hora_fin.strftime('%H:%M:%S'), precio, sala, tecnologia, funcion_id))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_funcion(funcion_id):
    """Eliminar una función"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM funciones WHERE id = %s", (funcion_id,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_generos():
    """Obtener todos los géneros"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM generos ORDER BY nombre")
    generos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return generos

def get_genero_by_id(genero_id):
    """Obtener un género por ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM generos WHERE id = %s", (genero_id,))
    genero = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return genero

def create_genero(nombre):
    """Crear un nuevo género"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO generos (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_genero(genero_id, nombre):
    """Actualizar un género"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE generos SET nombre=%s WHERE id=%s", (nombre, genero_id))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_genero(genero_id):
    """Eliminar un género"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM generos WHERE id = %s", (genero_id,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_actores():
    """Obtener todos los actores"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM actores ORDER BY nombre")
    actores = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return actores

def get_actor_by_id(actor_id):
    """Obtener un actor por ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM actores WHERE id = %s", (actor_id,))
    actor = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return actor

def create_actor(nombre):
    """Crear un nuevo actor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO actores (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_actor(actor_id, nombre):
    """Actualizar un actor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE actores SET nombre=%s WHERE id=%s", (nombre, actor_id))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_actor(actor_id):
    """Eliminar un actor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM actores WHERE id = %s", (actor_id,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def get_all_asientos():
    """Obtener todos los asientos con detalles"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT a.*, ta.nombre as tipo_nombre, ta.precio as tipo_precio
        FROM asientos a
        JOIN tipos_asientos ta ON a.tipo_id = ta.id
        ORDER BY a.fila, a.columna
    """
    
    cursor.execute(query)
    asientos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return asientos

def get_asiento_by_id(asiento_id):
    """Obtener un asiento por ID"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT a.*, ta.nombre as tipo_nombre, ta.precio as tipo_precio
        FROM asientos a
        JOIN tipos_asientos ta ON a.tipo_id = ta.id
        WHERE a.id = %s
    """, (asiento_id,))
    
    asiento = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return asiento

def get_tipos_asientos():
    """Obtener todos los tipos de asientos"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM tipos_asientos ORDER BY nombre")
    tipos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return tipos

def create_asiento(numero, fila, columna, tipo_id):
    """Crear un nuevo asiento"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO asientos (numero, fila, columna, tipo_id)
            VALUES (%s, %s, %s, %s)
        """, (numero, fila, columna, tipo_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_asiento(asiento_id, numero, fila, columna, tipo_id):
    """Actualizar un asiento"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE asientos 
            SET numero=%s, fila=%s, columna=%s, tipo_id=%s
            WHERE id=%s
        """, (numero, fila, columna, tipo_id, asiento_id))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def delete_asiento(asiento_id):
    """Eliminar un asiento"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM asientos WHERE id = %s", (asiento_id,))
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# ==========================================
# FUNCIONES PARA AUTENTICACIÓN DE USUARIOS
# ==========================================

def hash_password(password):
    """Hashear contraseña con bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, password_hash):
    """Verificar contraseña contra hash bcrypt"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def email_exists(email):
    """Verificar si un email ya está registrado"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email.lower(),))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return result is not None

def create_usuario(email, nombre, apellido, password, telefono=None, ciudad=None, rol='usuario'):
    """Crear un nuevo usuario registrado"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO usuarios (email, nombre, apellido, password_hash, telefono, ciudad, rol, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo')
        """, (email.lower(), nombre, apellido, password_hash, telefono, ciudad, rol))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error creating usuario: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_usuario_by_email(email):
    """Obtener usuario por email (para login - funciona para usuarios y admins)"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT id, email, nombre, apellido, password_hash, telefono, ciudad, rol,
               fecha_registro, ultimo_acceso, estado
        FROM usuarios 
        WHERE email = %s AND estado = 'activo'
    """, (email.lower(),))
    
    usuario = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return usuario

def get_usuario_by_id(user_id):
    """Obtener datos del perfil de usuario"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT id, email, nombre, apellido, telefono, ciudad, rol,
               fecha_registro, ultimo_acceso, estado
        FROM usuarios 
        WHERE id = %s
    """, (user_id,))
    
    usuario = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return usuario

def update_usuario_profile(user_id, nombre=None, apellido=None, telefono=None, ciudad=None):
    """Actualizar datos del perfil de usuario"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        updates = []
        params = []
        
        if nombre is not None:
            updates.append("nombre = %s")
            params.append(nombre)
        if apellido is not None:
            updates.append("apellido = %s")
            params.append(apellido)
        if telefono is not None:
            updates.append("telefono = %s")
            params.append(telefono)
        if ciudad is not None:
            updates.append("ciudad = %s")
            params.append(ciudad)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s"
        
        cursor.execute(query, params)
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error updating usuario profile: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def update_usuario_last_access(user_id):
    """Actualizar timestamp de último acceso"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE usuarios 
            SET ultimo_acceso = NOW() 
            WHERE id = %s
        """, (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Error updating last access: {e}")
    finally:
        cursor.close()
        conn.close()

def get_user_compras(user_id):
    """Obtener historial de compras del usuario"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT 
            t.id,
            t.codigo,
            t.total,
            t.estado,
            t.fecha_compra,
            f.fecha,
            f.hora,
            f.sala,
            f.tecnologia,
            p.titulo as pelicula_titulo,
            p.clasificacion,
            p.imagen_url,
            COUNT(dt.asiento_id) as cantidad_asientos
        FROM tiquetes t
        JOIN funciones f ON t.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        LEFT JOIN detalle_tiquete dt ON t.id = dt.tiquete_id
        WHERE t.email = (SELECT email FROM usuarios WHERE id = %s)
        GROUP BY t.id
        ORDER BY t.fecha_compra DESC
    """
    
    cursor.execute(query, (user_id,))
    compras = cursor.fetchall()
    
    # Convertir tipos no serializables
    for c in compras:
        if c.get('fecha'):
            c['fecha'] = str(c['fecha'])
        if c.get('hora'):
            c['hora'] = str(c['hora'])
        if c.get('total'):
            c['total'] = float(c['total'])
        if c.get('fecha_compra'):
            c['fecha_compra'] = str(c['fecha_compra'])
    
    cursor.close()
    conn.close()
    return compras

def get_user_compra_detalle(user_id, ticket_id):
    """Obtener detalles de una compra específica del usuario"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Primero verificar que el ticket pertenece al usuario
    cursor.execute("""
        SELECT u.id FROM usuarios u
        JOIN tiquetes t ON t.email = u.email
        WHERE u.id = %s AND t.id = %s
    """, (user_id, ticket_id))
    
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return None
    
    # Obtener detalles del ticket
    query = """
        SELECT 
            t.id,
            t.codigo,
            t.email,
            t.total,
            t.estado,
            t.fecha_compra,
            f.fecha,
            f.hora,
            f.sala,
            f.tecnologia,
            p.titulo as pelicula_titulo,
            p.clasificacion,
            p.descripcion,
            p.director,
            p.imagen_url,
            GROUP_CONCAT(a.numero ORDER BY a.fila, a.columna SEPARATOR ', ') as asientos
        FROM tiquetes t
        JOIN funciones f ON t.funcion_id = f.id
        JOIN peliculas p ON f.pelicula_id = p.id
        LEFT JOIN detalle_tiquete dt ON t.id = dt.tiquete_id
        LEFT JOIN asientos a ON dt.asiento_id = a.id
        WHERE t.id = %s
        GROUP BY t.id
    """
    
    cursor.execute(query, (ticket_id,))
    compra = cursor.fetchone()
    
    if compra:
        if compra.get('fecha'):
            compra['fecha'] = str(compra['fecha'])
        if compra.get('hora'):
            compra['hora'] = str(compra['hora'])
        if compra.get('total'):
            compra['total'] = float(compra['total'])
        if compra.get('fecha_compra'):
            compra['fecha_compra'] = str(compra['fecha_compra'])
    
    cursor.close()
    conn.close()
    return compra

def process_purchase_with_user(funcion_id, asiento_ids, user_id, ticket_code, total=0):
    """
    Procesar compra vinculada a usuario registrado.
    Retorna ticket_id si es exitoso, None si falla.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Obtener email del usuario
        cursor.execute("SELECT email FROM usuarios WHERE id = %s", (user_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"Usuario {user_id} no encontrado")
            return None
        
        email = usuario[0]
        
        # 1. Insertar en tiquetes
        insert_ticket = """
            INSERT INTO tiquetes (codigo, funcion_id, email, total, estado)
            VALUES (%s, %s, %s, %s, 'activo')
        """
        cursor.execute(insert_ticket, (ticket_code, funcion_id, email, total))
        conn.commit()
        ticket_id = cursor.lastrowid
        
        print(f"Ticket inserted with ID: {ticket_id}")
        
        # 2. Insertar en detalle_tiquete para cada asiento
        insert_detail = """
            INSERT INTO detalle_tiquete (tiquete_id, asiento_id, funcion_id)
            VALUES (%s, %s, %s)
        """
        for asiento_id in asiento_ids:
            cursor.execute(insert_detail, (ticket_id, asiento_id, funcion_id))
        
        conn.commit()
        
        # 3. Limpiar reservas temporales
        for asiento_id in asiento_ids:
            delete_query = "DELETE FROM reservas_temporales WHERE funcion_id = %s AND asiento_id = %s"
            cursor.execute(delete_query, (funcion_id, asiento_id))
        
        conn.commit()
        print(f"Purchase processed. Ticket ID: {ticket_id}")
        return ticket_id
        
    except Exception as e:
        print(f"Error processing purchase: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get_admin_by_email(email):
    """Obtener admin por email - busca usuario con rol='admin'
    (función mantenida para compatibilidad con app.py)"""
    return get_usuario_by_email(email)