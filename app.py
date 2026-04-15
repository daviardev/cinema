from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_mail import Mail
from datetime import timedelta
from functools import wraps
import os
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
                get_dashboard_stats, hash_password, verify_password, email_exists, create_usuario, get_usuario_by_email,
                get_usuario_by_id, get_user_compras, get_user_compra_detalle, process_purchase_with_user,
                update_usuario_last_access, get_admin_by_email, initialize_database)

app = Flask(__name__, static_folder='static', static_url_path='')

# Detectar entorno (production vs development)
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
IS_PRODUCTION = FLASK_ENV == 'production'

# Configurar secret key (desde variable de entorno o fallback)
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_super_secret_cinema_vox_2025_dev')

# Configuración de sesión (optimizada para Railway)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=4)
app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION  # True en Railway (HTTPS), False en localhost
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.after_request
def refresh_session(response):
    """Refrescar la sesión después de cada request para asegurar persistencia"""
    session.modified = True
    return response

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

# ==========================================
# DECORADORES PARA AUTORIZACIÓN
# ==========================================

def login_required(f):
    """Decorador para proteger rutas - requiere usuario autenticado (usuario o admin)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        
        # Actualizar timestamp de último acceso
        update_usuario_last_access(session['user_id'])
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para proteger rutas admin - requiere rol='admin'"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_rol') != 'admin':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# RUTAS DE AUTENTICACIÓN
# ==========================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember')
        
        # Intentar login - funciona para usuarios y admins
        usuario = get_usuario_by_email(email)
        if usuario and verify_password(password, usuario['password_hash']):
            # Autenticación exitosa
            session['user_id'] = usuario['id']
            session['user_email'] = usuario['email']
            session['user_nombre'] = usuario['nombre']
            session['user_rol'] = usuario.get('rol', 'usuario')  # Guardar el rol
            
            if remember:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            
            # Si es admin, redirigir al panel de admin
            if session['user_rol'] == 'admin':
                return redirect(url_for('admin_index'))
            
            # Si es usuario regular, manejar redirección a checkout si hay compra pendiente
            next_page = request.args.get('next')
            if next_page == 'checkout':
                return redirect(url_for('checkout'))
            
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('mi_cuenta'))
        
        return render_template('login.html', error='Email o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '') or request.form.get('apellidos', '')  # Support both
        apellido = apellido.strip()
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        ciudad = request.form.get('ciudad', '').strip()
        telefono = request.form.get('telefono', '').strip()
        
        # Validaciones
        if not nombre or not apellido or not email or not password:
            return render_template('registro.html', error='Todos los campos obligatorios deben completarse')
        
        if password != password_confirm:
            return render_template('registro.html', error='Las contraseñas no coinciden')
        
        if len(password) < 8:
            return render_template('registro.html', error='La contraseña debe tener al menos 8 caracteres')
        
        if email_exists(email):
            return render_template('registro.html', error='Este email ya está registrado')
        
        # Crear usuario
        if create_usuario(email, nombre, apellido, password, telefono, ciudad):
            # Auto-login después de registro
            usuario = get_usuario_by_email(email)
            session['user_id'] = usuario['id']
            session['user_email'] = usuario['email']
            session['user_nombre'] = usuario['nombre']
            
            # Manejar redirección a checkout si hay compra pendiente
            next_page = request.args.get('next')
            if next_page == 'checkout':
                return redirect(url_for('checkout'))
            
            return redirect(url_for('mi_cuenta'))
        else:
            return render_template('registro.html', error='Error al crear la cuenta. Intenta nuevamente.')
    
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/inicializar-bd', methods=['POST'])
def inicializar_bd():
    """Endpoint para inicializar la base de datos con datos básicos"""
    try:
        result = initialize_database()
        if result:
            return jsonify({'success': True, 'message': 'Base de datos inicializada correctamente'}), 200
        else:
            return jsonify({'success': False, 'error': 'Error al inicializar la base de datos'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/checkout')
@login_required
def checkout():
    """
    Ruta para retornar después de autenticación en el flujo de compra.
    Redirige al índice principal donde JavaScript restaurará el estado de compra.
    """
    # Obtener el email del usuario autenticado
    user_email = session.get('user_email', '')
    
    # Redirigir al índice con instrucción de completar compra
    # El cliente restaurará el estado desde localStorage y abrirá el modal de email
    response = redirect(url_for('index'))
    response.set_cookie('complete_purchase', '1', max_age=10)  # 10 segundos
    return response

@app.route('/mi-cuenta')
@login_required
def mi_cuenta():
    # Si es admin, redirigir al panel de admin
    if session.get('user_rol') == 'admin':
        return redirect(url_for('admin_index'))
    
    usuario = get_usuario_by_id(session['user_id'])
    compras = get_user_compras(session['user_id'])
    return render_template('usuario/dashboard.html', usuario=usuario, compras=compras)

@app.route('/descargar-ticket/<int:ticket_id>')
@login_required
def descargar_ticket(ticket_id):
    compra = get_user_compra_detalle(session['user_id'], ticket_id)
    
    if not compra:
        return redirect(url_for('mi_cuenta'))
    
    # Por ahora, renderizar una página con el QR
    return render_template('usuario/ticket.html', compra=compra)

@app.route('/api/auth-status')
def api_auth_status():
    """Verificar estado de autenticación del usuario"""
    try:
        if 'user_id' in session:
            return jsonify({
                'authenticated': True,
                'user_id': session['user_id'],
                'user_name': session.get('user_nombre', 'Usuario'),
                'user_email': session.get('user_email'),
                'user_rol': session.get('user_rol', 'usuario')
            })
    except Exception as e:
        print(f"Error in auth-status: {e}")
    
    return jsonify({'authenticated': False})

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    from datetime import datetime
    stats = get_dashboard_stats()
    return render_template('admin/dashboard.html', stats=stats, now=datetime.now())

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
        
        print(f"[DEBUG] procesar_compra - Datos recibidos: funcion={funcion_id}, asientos={asiento_ids}, email={email}, code={ticket_code}, total={total}")
        
        if not funcion_id or not asiento_ids or not email or not ticket_code:
            print(f"[ERROR] Campos faltantes")
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Procesar la compra
        ticket_id = process_purchase(funcion_id, asiento_ids, email, ticket_code, total)
        
        print(f"[DEBUG] process_purchase retornó: {ticket_id}")
        
        if ticket_id:
            # Intentar enviar email (pero no fallar si hay error)
            try:
                funcion_data = get_funcion_with_details(funcion_id)
                if funcion_data:
                    try:
                        asientos_map = get_asientos_disponibles(funcion_id)
                        asientos_list = [asiento for asiento in asientos_map if int(asiento['id']) in asiento_ids]
                        send_ticket_email(email, ticket_code, funcion_data.get('pelicula', 'Película'), 
                                        funcion_data, asientos_list, mail)
                        print(f"Email enviado a {email}")
                    except Exception as asiento_error:
                        print(f"Advertencia: Error obteniendo/enviando asientos: {asiento_error}")
            except Exception as email_error:
                print(f"Advertencia: Error preparando email: {email_error}")
            
            # SIEMPRE devolver éxito si el ticket se guardó
            return jsonify({
                'success': True, 
                'ticket_id': ticket_id,
                'ticket_code': ticket_code,
                'message': 'Compra procesada exitosamente!'
            }), 201
        else:
            print(f"[ERROR] process_purchase devolvió None/False")
            return jsonify({'success': False, 'error': 'No se pudo procesar la compra'}), 500
    except Exception as e:
        print(f"[ERROR] Exception en procesar_compra: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Error del servidor: {str(e)}'}), 500

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
@admin_required
def admin_index():
    try:
        from datetime import datetime
        stats = get_dashboard_stats()
        return render_template('admin/dashboard.html', stats=stats, now=datetime.now())
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard_alt():
    """Alias para /admin - redirige al dashboard"""
    try:
        from datetime import datetime
        stats = get_dashboard_stats()
        return render_template('admin/dashboard.html', stats=stats, now=datetime.now())
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/dashboard.html')
@admin_required
def admin_dashboard_html():
    """Manejo de acceso con extensión .html - redirige a /admin"""
    return redirect(url_for('admin_index'))

@app.route('/admin/peliculas')
@admin_required
def admin_peliculas():
    try:
        peliculas = get_all_peliculas()
        return render_template('admin/peliculas.html', peliculas=peliculas)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/peliculas/crear', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
def admin_eliminar_pelicula(id):
    try:
        delete_pelicula(id)
        return jsonify({'success': True, 'message': 'Película eliminada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/funciones')
@admin_required
def admin_funciones():
    try:
        funciones = get_all_funciones()
        return render_template('admin/funciones.html', funciones=funciones)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/funciones/crear', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
def admin_eliminar_funcion(id):
    try:
        delete_funcion(id)
        return jsonify({'success': True, 'message': 'Función eliminada exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/validar-funcion', methods=['POST'])
@admin_required
def validar_funcion():
    """Validar si una función puede crearse sin conflictos de horarios"""
    try:
        from datetime import datetime, timedelta
        
        data = request.get_json()
        pelicula_id = data.get('pelicula_id')
        fecha = data.get('fecha')
        hora = data.get('hora')
        sala = data.get('sala')
        
        if not all([pelicula_id, fecha, hora, sala]):
            return jsonify({'valid': False, 'error': 'Faltan parámetros'})
        
        # Obtener duración de pelicula y calcular hora_fin
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT duracion FROM peliculas WHERE id = %s", (pelicula_id,))
        pelicula = cursor.fetchone()
        
        if not pelicula:
            cursor.close()
            conn.close()
            return jsonify({'valid': False, 'error': 'Película no encontrada'})
        
        duracion = pelicula['duracion']
        hora_obj = datetime.strptime(hora, '%H:%M').time()
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_inicio = datetime.combine(fecha_obj, hora_obj)
        hora_fin = (hora_inicio + timedelta(minutes=duracion)).time()
        
        # Buscar conflictos
        cursor.execute("""
            SELECT id, p.titulo,   f.hora, f.hora_fin
            FROM funciones f
            JOIN peliculas p ON f.pelicula_id = p.id
            WHERE f.sala = %s AND f.fecha = %s
        """, (sala, fecha))
        
        conflictos = []
        for funcion in cursor.fetchall():
            h_inicio = datetime.combine(fecha_obj, funcion['hora'])
            h_fin = datetime.combine(fecha_obj, funcion['hora_fin'])
            
            if hora_inicio < h_fin and (hora_inicio + timedelta(minutes=duracion)) > h_inicio:
                conflictos.append({
                    'pelicula': funcion['titulo'],
                    'hora': str(funcion['hora']),
                    'hora_fin': str(funcion['hora_fin'])
                })
        
        cursor.close()
        conn.close()
        
        if conflictos:
            return jsonify({
                'valid': False,
                'error': f'Conflicto de horarios en {sala}',
                'conflictos': conflictos
            })
        
        return jsonify({
            'valid': True,
            'hora_fin': hora_fin.strftime('%H:%M'),
            'message': f'Función válida: {hora} - {hora_fin.strftime("%H:%M")} ({duracion} min)'
        })
        
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

@app.route('/admin/generos')
@admin_required
def admin_generos():
    try:
        generos = get_all_generos()
        return render_template('admin/generos.html', generos=generos)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/generos/crear', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
def admin_eliminar_genero(id):
    try:
        delete_genero(id)
        return jsonify({'success': True, 'message': 'Género eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/actores')
@admin_required
def admin_actores():
    try:
        actores = get_all_actores()
        return render_template('admin/actores.html', actores=actores)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/actores/crear', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
def admin_eliminar_actor(id):
    try:
        delete_actor(id)
        return jsonify({'success': True, 'message': 'Actor eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/asientos')
@admin_required
def admin_asientos():
    try:
        asientos = get_all_asientos()
        tipos_asientos = get_tipos_asientos()
        return render_template('admin/asientos.html', asientos=asientos, tipos_asientos=tipos_asientos)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/admin/asientos/crear', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
def admin_eliminar_asiento(id):
    try:
        delete_asiento(id)
        return jsonify({'success': True, 'message': 'Asiento eliminado exitosamente'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)