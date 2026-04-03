import mysql.connector

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