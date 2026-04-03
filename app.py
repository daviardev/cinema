from flask import Flask, render_template, jsonify, request
from flask_mail import Mail
from config import (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, 
                    MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME, MAIL_PASSWORD, EMAIL_DEFAULT_SENDER)

from db import (get_db_connection, get_peliculas_cartelera, get_funciones_por_pelicula, get_asientos_disponibles, 
                create_reserva_temporal, delete_reserva_temporal, process_purchase,
                get_ticket_by_code, mark_ticket_used, send_ticket_email, get_funcion_with_details)

app = Flask(__name__, static_folder='static', static_url_path='')

# Configurar Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = EMAIL_DEFAULT_SENDER

mail = Mail(app)

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

if __name__ == '__main__':
    app.run(debug=True)