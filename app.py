from flask import Flask, render_template, jsonify, request
from flask_mail import Mail
from datetime import timedelta
from config import (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, 
                    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, EMAIL_DEFAULT_SENDER)

from db import (get_db_connection, get_peliculas_cartelera, get_funciones_por_pelicula, get_asientos_disponibles, 
                create_reserva_temporal, delete_reserva_temporal, process_purchase,
                get_ticket_by_code, mark_ticket_used, send_ticket_email, get_funcion_with_details,
                get_all_peliculas, get_pelicula_by_id, create_pelicula, update_pelicula, delete_pelicula,
                get_all_funciones, get_funcion_by_id, create_funcion, update_funcion, delete_funcion,
                get_all_generos, create_genero, update_genero, delete_genero,
                get_all_actores, create_actor, update_actor, delete_actor,
                get_all_asientos, get_asiento_by_id, get_tipos_asientos, create_asiento, update_asiento, delete_asiento,
                get_dashboard_stats)

app = Flask(__name__, static_folder='static', static_url_path='')

# Configurar Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = EMAIL_DEFAULT_SENDER

mail = Mail(app)

# Agregar filtro strftime para Jinja2
@app.template_filter('strftime')
def strftime_filter(date, format_string):
    if date is None:
        return ''
    if hasattr(date, 'strftime'):
        return date.strftime(format_string)
    # Manejar timedelta (para horas)
    if isinstance(date, timedelta):
        # Convertir timedelta a time
        from datetime import datetime
        total_seconds = int(date.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_obj = datetime(1900, 1, 1, hours, minutes, seconds).time()
        return time_obj.strftime(format_string)
    # Si es un string, intentar convertirlo a datetime
    if isinstance(date, str):
        from datetime import datetime
        try:
            # Intentar diferentes formatos de fecha
            for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%Y', '%d/%m/%Y %H:%M:%S']:
                try:
                    dt = datetime.strptime(date, fmt)
                    return dt.strftime(format_string)
                except ValueError:
                    continue
            return date  # Si no se puede parsear, devolver el string original
        except:
            return str(date)
    return str(date)

@app.after_request
def set_no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/peliculas')
def peliculas():
    try:
        peliculas_data = get_peliculas_cartelera()
        return jsonify(peliculas_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/funciones/<int:pelicula_id>')
def funciones(pelicula_id):
    try:
        funciones_data = get_funciones_por_pelicula(pelicula_id)
        return jsonify(funciones_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/asientos/<int:funcion_id>')
def asientos(funcion_id):
    try:
        asientos_data = get_asientos_disponibles(funcion_id)
        return jsonify(asientos_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reserva-temporal/crear', methods=['POST'])
def crear_reserva():
    try:
        data = request.json
        funcion_id = data.get('funcion_id')
        asiento_id = data.get('asiento_id')
        
        if not funcion_id or not asiento_id:
            return jsonify({'error': 'Missing funcion_id or asiento_id'}), 400
        
        result = create_reserva_temporal(funcion_id, asiento_id)
        if result:
            return jsonify({'success': True, 'message': 'Reserva temporal creada'}), 201
        else:
            return jsonify({'error': 'No se pudo crear la reserva'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reserva-temporal/limpiar', methods=['POST'])
def limpiar_reserva():
    try:
        data = request.json
        funcion_id = data.get('funcion_id')
        asiento_id = data.get('asiento_id')
        
        if not funcion_id or not asiento_id:
            return jsonify({'error': 'Missing funcion_id or asiento_id'}), 400
        
        result = delete_reserva_temporal(funcion_id, asiento_id)
        if result:
            return jsonify({'success': True, 'message': 'Reserva temporal eliminada'}), 200
        else:
            return jsonify({'error': 'No se pudo eliminar la reserva'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/procesar-compra', methods=['POST'])
def procesar_compra():
    try:
        data = request.json
        funcion_id = data.get('funcion_id')
        asiento_ids = data.get('asiento_ids')  # Lista de IDs
        email = data.get('email')
        ticket_code = data.get('ticket_code')
        total = float(data.get('total', 0))
        
        if not funcion_id or not asiento_ids or not email or not ticket_code:
            return jsonify({'error': 'Missing required fields'}), 400
        
        ticket_id = process_purchase(funcion_id, asiento_ids, email, ticket_code, total)
        
        if ticket_id:
            # Obtener detalles de la función y película para el email
            try:
                funcion_data = get_funcion_with_details(funcion_id)
                if funcion_data:
                    # Obtener asientos para el email
                    asientos_map = get_asientos_disponibles(funcion_id)
                    asientos_list = [asiento for asiento in asientos_map if int(asiento['id']) in asiento_ids]
                    
                    # Enviar email con el ticket
                    send_ticket_email(email, ticket_code, funcion_data.get('pelicula', 'Película'), 
                                    funcion_data, asientos_list, mail)
            except Exception as email_error:
                print(f"Error enviando email: {email_error}")
                # No fallar la compra si hay error en el email
            
            return jsonify({
                'success': True, 
                'ticket_id': ticket_id,
                'ticket_code': ticket_code,
                'message': 'Compra procesada exitosamente. Email enviado.'
            }), 201
        else:
            return jsonify({'error': 'No se pudo procesar la compra'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verificar-ticket/<codigo>', methods=['GET'])
def verificar_ticket(codigo):
    try:
        ticket_data = get_ticket_by_code(codigo)
        
        if ticket_data:
            return jsonify({
                'success': True,
                'ticket': ticket_data
            }), 200
        else:
            return jsonify({'error': 'Ticket no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/canjear-ticket/<codigo>', methods=['POST'])
def canjear_ticket(codigo):
    try:
        # Verificar que el ticket existe
        ticket_data = get_ticket_by_code(codigo)
        
        if not ticket_data:
            return jsonify({'error': 'Ticket no encontrado'}), 404
        
        if ticket_data.get('estado') == 'canjeado':
            return jsonify({'error': 'Este ticket ya ha sido canjeado'}), 400
        
        # Marcar ticket como usado
        success = mark_ticket_used(codigo)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Ticket canjeado exitosamente'
            }), 200
        else:
            return jsonify({'error': 'No se pudo canjear el ticket'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reenviar-ticket/<codigo>', methods=['POST'])
def reenviar_ticket(codigo):
    try:
        data = request.json or {}
        email = data.get('email')
        
        # Verificar que el ticket existe
        ticket_data = get_ticket_by_code(codigo)
        
        if not ticket_data:
            return jsonify({'error': 'Ticket no encontrado'}), 404
        
        recipient_email = email or ticket_data.get('email')
        
        if not recipient_email:
            return jsonify({'error': 'Email requerido'}), 400
        
        # Obtener detalles de la función para el email
        try:
            funcion_data = get_funcion_with_details(ticket_data.get('funcion_id'))
            if funcion_data:
                asientos_list = ticket_data.get('asientos', [])
                
                # Reenviar email
                send_ticket_email(recipient_email, codigo, funcion_data.get('pelicula', 'Película'),
                                funcion_data, asientos_list, mail)
                
                return jsonify({
                    'success': True,
                    'message': f'Ticket reenviado a {recipient_email}'
                }), 200
        except Exception as email_error:
            return jsonify({'error': f'Error enviando email: {str(email_error)}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mis-tiquetes', methods=['GET'])
def mis_tiquetes():
    try:
        email = request.args.get('email', '').strip()
        
        if not email:
            return jsonify({'success': False, 'error': 'Email requerido'}), 400
        
        try:
            con = get_db_connection()
            cursor = con.cursor(dictionary=True)
            
            # Obtener tiquetes del usuario
            cursor.execute('''
                SELECT 
                    t.id,
                    t.codigo,
                    t.estado,
                    t.email,
                    t.total,
                    f.fecha,
                    f.hora,
                    f.sala,
                    p.titulo as pelicula_titulo,
                    GROUP_CONCAT(a.numero ORDER BY a.fila, a.columna SEPARATOR ', ') as asientos_str,
                    JSON_ARRAYAGG(
                        JSON_OBJECT(
                            'id', a.id,
                            'numero', a.numero,
                            'fila', a.fila,
                            'columna', a.columna
                        )
                    ) as asientos_json
                FROM tiquetes t
                JOIN funciones f ON t.funcion_id = f.id
                JOIN peliculas p ON f.pelicula_id = p.id
                LEFT JOIN detalle_tiquete dt ON t.id = dt.tiquete_id
                LEFT JOIN asientos a ON dt.asiento_id = a.id
                WHERE LOWER(t.email) = LOWER(%s)
                GROUP BY t.id
                ORDER BY t.fecha_compra DESC, t.id DESC
            ''', (email,))
            
            tickets = cursor.fetchall()
            cursor.close()
            con.close()
            
            if not tickets:
                return jsonify({
                    'success': True,
                    'tickets': []
                }), 200
            
            # Procesar los datos
            formatted_tickets = []
            for t in tickets:
                # Parsear asientos JSON
                asientos = []
                try:
                    if t.get('asientos_json'):
                        import json
                        asientos = json.loads(t['asientos_json'])
                except:
                    asientos = []
                
                formatted_tickets.append({
                    'id': t['id'],
                    'codigo': t['codigo'],
                    'estado': t['estado'],
                    'email': t['email'],
                    'total': float(t['total'] or 0),
                    'fecha': str(t['fecha']),
                    'hora': str(t['hora']),
                    'sala': t['sala'],
                    'pelicula_titulo': t['pelicula_titulo'],
                    'asientos': asientos
                })
            
            return jsonify({
                'success': True,
                'tickets': formatted_tickets
            }), 200
            
        except Exception as db_error:
            return jsonify({'success': False, 'error': f'Error en BD: {str(db_error)}'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==========================================
# DASHBOARD ADMINISTRATIVO
# ==========================================

@app.route('/admin')
def admin_dashboard():
    try:
        from datetime import datetime
        stats = get_dashboard_stats()
        return render_template('admin/dashboard.html', stats=stats, now=datetime.now())
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/peliculas')
def admin_peliculas():
    try:
        peliculas = get_all_peliculas()
        return render_template('admin/peliculas.html', peliculas=peliculas)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/peliculas/crear', methods=['GET', 'POST'])
def admin_crear_pelicula():
    if request.method == 'POST':
        try:
            data = request.form
            titulo = data.get('titulo')
            descripcion = data.get('descripcion')
            duracion = int(data.get('duracion', 0))
            clasificacion = data.get('clasificacion')
            imagen_url = data.get('imagen_url')
            anio = int(data.get('anio', 0))
            director = data.get('director')
            puntuacion = float(data.get('puntuacion', 0))
            generos = request.form.getlist('generos')
            actores = request.form.getlist('actores')
            
            create_pelicula(titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion, generos, actores)
            return jsonify({'success': True, 'message': 'Película creada exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        generos = get_all_generos()
        actores = get_all_actores()
        return render_template('admin/crear_pelicula.html', generos=generos, actores=actores)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/peliculas/editar/<int:id>', methods=['GET', 'POST'])
def admin_editar_pelicula(id):
    if request.method == 'POST':
        try:
            data = request.form
            titulo = data.get('titulo')
            descripcion = data.get('descripcion')
            duracion = int(data.get('duracion', 0))
            clasificacion = data.get('clasificacion')
            imagen_url = data.get('imagen_url')
            anio = int(data.get('anio', 0))
            director = data.get('director')
            puntuacion = float(data.get('puntuacion', 0))
            generos = request.form.getlist('generos')
            actores = request.form.getlist('actores')
            
            update_pelicula(id, titulo, descripcion, duracion, clasificacion, imagen_url, anio, director, puntuacion, generos, actores)
            return jsonify({'success': True, 'message': 'Película actualizada exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        pelicula = get_pelicula_by_id(id)
        # Extract IDs for template checking
        if pelicula.get('generos'):
            pelicula['generos_ids'] = [g['id'] if isinstance(g, dict) else g.id for g in pelicula['generos']]
        else:
            pelicula['generos_ids'] = []
        if pelicula.get('actores'):
            pelicula['actores_ids'] = [a['id'] if isinstance(a, dict) else a.id for a in pelicula['actores']]
        else:
            pelicula['actores_ids'] = []
        generos = get_all_generos()
        actores = get_all_actores()
        return render_template('admin/editar_pelicula.html', pelicula=pelicula, generos=generos, actores=actores)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/peliculas/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_pelicula(id):
    try:
        delete_pelicula(id)
        return jsonify({'success': True, 'message': 'Película eliminada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/funciones')
def admin_funciones():
    try:
        funciones = get_all_funciones()
        return render_template('admin/funciones.html', funciones=funciones)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/funciones/crear', methods=['GET', 'POST'])
def admin_crear_funcion():
    if request.method == 'POST':
        try:
            data = request.form
            pelicula_id = int(data.get('pelicula_id'))
            fecha = data.get('fecha')
            hora = data.get('hora')
            precio = float(data.get('precio', 0))
            sala = data.get('sala')
            tecnologia = data.get('tecnologia')
            
            create_funcion(pelicula_id, fecha, hora, precio, sala, tecnologia)
            return jsonify({'success': True, 'message': 'Función creada exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        peliculas = get_all_peliculas()
        return render_template('admin/crear_funcion.html', peliculas=peliculas)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/funciones/editar/<int:id>', methods=['GET', 'POST'])
def admin_editar_funcion(id):
    if request.method == 'POST':
        try:
            data = request.form
            pelicula_id = int(data.get('pelicula_id'))
            fecha = data.get('fecha')
            hora = data.get('hora')
            precio = float(data.get('precio', 0))
            sala = data.get('sala')
            tecnologia = data.get('tecnologia')
            
            update_funcion(id, pelicula_id, fecha, hora, precio, sala, tecnologia)
            return jsonify({'success': True, 'message': 'Función actualizada exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        funcion = get_funcion_by_id(id)
        peliculas = get_all_peliculas()
        return render_template('admin/editar_funcion.html', funcion=funcion, peliculas=peliculas)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/funciones/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_funcion(id):
    try:
        delete_funcion(id)
        return jsonify({'success': True, 'message': 'Función eliminada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/generos')
def admin_generos():
    try:
        generos = get_all_generos()
        return render_template('admin/generos.html', generos=generos)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/generos/crear', methods=['GET', 'POST'])
def admin_crear_genero():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            create_genero(nombre)
            return jsonify({'success': True, 'message': 'Género creado exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('admin/crear_genero.html')

@app.route('/admin/generos/editar/<int:id>', methods=['GET', 'POST'])
def admin_editar_genero(id):
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            update_genero(id, nombre)
            return jsonify({'success': True, 'message': 'Género actualizado exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        genero = get_genero_by_id(id)
        return render_template('admin/editar_genero.html', genero=genero)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/generos/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_genero(id):
    try:
        delete_genero(id)
        return jsonify({'success': True, 'message': 'Género eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/actores')
def admin_actores():
    try:
        actores = get_all_actores()
        return render_template('admin/actores.html', actores=actores)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/actores/crear', methods=['GET', 'POST'])
def admin_crear_actor():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            create_actor(nombre)
            return jsonify({'success': True, 'message': 'Actor creado exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    return render_template('admin/crear_actor.html')

@app.route('/admin/actores/editar/<int:id>', methods=['GET', 'POST'])
def admin_editar_actor(id):
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            update_actor(id, nombre)
            return jsonify({'success': True, 'message': 'Actor actualizado exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        actor = get_actor_by_id(id)
        return render_template('admin/editar_actor.html', actor=actor)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/actores/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_actor(id):
    try:
        delete_actor(id)
        return jsonify({'success': True, 'message': 'Actor eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/asientos')
def admin_asientos():
    try:
        asientos = get_all_asientos()
        tipos_asientos = get_tipos_asientos()
        return render_template('admin/asientos.html', asientos=asientos, tipos_asientos=tipos_asientos)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/asientos/crear', methods=['GET', 'POST'])
def admin_crear_asiento():
    if request.method == 'POST':
        try:
            data = request.form
            numero = data.get('numero')
            fila = data.get('fila')
            columna = int(data.get('columna', 0))
            tipo_id = int(data.get('tipo_id'))
            
            create_asiento(numero, fila, columna, tipo_id)
            return jsonify({'success': True, 'message': 'Asiento creado exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        tipos_asientos = get_tipos_asientos()
        return render_template('admin/crear_asiento.html', tipos_asientos=tipos_asientos)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/asientos/editar/<int:id>', methods=['GET', 'POST'])
def admin_editar_asiento(id):
    if request.method == 'POST':
        try:
            data = request.form
            numero = data.get('numero')
            fila = data.get('fila')
            columna = int(data.get('columna', 0))
            tipo_id = int(data.get('tipo_id'))
            
            update_asiento(id, numero, fila, columna, tipo_id)
            return jsonify({'success': True, 'message': 'Asiento actualizado exitosamente'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    try:
        asiento = get_asiento_by_id(id)
        tipos_asientos = get_tipos_asientos()
        return render_template('admin/editar_asiento.html', asiento=asiento, tipos_asientos=tipos_asientos)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/asientos/eliminar/<int:id>', methods=['POST'])
def admin_eliminar_asiento(id):
    try:
        delete_asiento(id)
        return jsonify({'success': True, 'message': 'Asiento eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)