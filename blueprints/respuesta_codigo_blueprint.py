from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, jsonify
import requests
import sys
import io

respuesta_codigo_bp = Blueprint('respuesta_codigo_bp', __name__, url_prefix='/respuestas')

# Probar código Python (sandbox local)
@respuesta_codigo_bp.route('/probar_codigo', methods=['POST'])
def probar_codigo():
    data = request.get_json()
    codigo = data.get('codigo', '')

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = mystdout = io.StringIO()
    sys.stderr = mystderr = io.StringIO()

    exito = True
    try:
        exec(codigo, {})
    except Exception as e:
        exito = False
        print(f"Error: {e}")

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    salida = mystdout.getvalue() + mystderr.getvalue()
    return jsonify({"salida": salida, "exito": exito})

# Crear una nueva respuesta de código
@respuesta_codigo_bp.route('/crear', methods=['GET', 'POST'])
def crear_respuesta():
    url_base_api = current_app.config["URL_BASE_API"]
    headers = {'Clave-De-Autenticacion': current_app.config['TOKEN']}
    api_url = f'{url_base_api}/respuestas'

    if request.method == 'POST':
        archivo_nombre = request.form.get('archivo_nombre')
        tiempo = request.form.get('tiempo')
        equipo_id = request.form.get('equipo_id')
        desafio_id = request.form.get('desafio_id')

        if not archivo_nombre or not tiempo or not equipo_id or not desafio_id:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('respuesta_codigo_bp.crear_respuesta'))

        respuesta_data = {
            'archivo_nombre': archivo_nombre,
            'tiempo': tiempo,
            'equipo_id': int(equipo_id),
            'desafio_id': int(desafio_id)
        }

        try:
            response = requests.post(api_url, json=respuesta_data, headers=headers)
            data = response.json()
            if response.status_code == 201:
                flash(data.get('message', 'Respuesta creada correctamente'), 'success')
                return redirect(url_for('respuesta_codigo_bp.listar_respuestas'))
            else:
                error_msg = data.get('error') or data.get('message') or 'Error desconocido'
                flash(error_msg, 'danger')
                return redirect(url_for('respuesta_codigo_bp.crear_respuesta'))
        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('respuesta_codigo_bp.crear_respuesta'))

    return render_template('crear_respuesta_codigo.html')

# Listar todas las respuestas
@respuesta_codigo_bp.route('/')
def listar_respuestas():
    url_base_api = current_app.config["URL_BASE_API"]
    headers = {'Clave-De-Autenticacion': current_app.config['TOKEN']}
    api_url = f'{url_base_api}/respuestas'

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            respuestas = response.json()
            return render_template('listar_respuestas_codigo.html', respuestas=respuestas)
        else:
            data = response.json()
            error_msg = data.get('error') or data.get('message') or "Error al obtener las respuestas"
            flash(error_msg, "danger")
            return render_template('listar_respuestas_codigo.html', respuestas=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_respuestas_codigo.html', respuestas=[])

# Obtener una respuesta por ID
@respuesta_codigo_bp.route('/<int:id>')
def obtener_respuesta(id):
    url_base_api = current_app.config["URL_BASE_API"]
    headers = {'Clave-De-Autenticacion': current_app.config['TOKEN']}
    api_url = f'{url_base_api}/respuestas/{id}'

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            respuesta = response.json()
            return render_template('actualizar_respuesta_codigo.html', respuesta=respuesta)
        else:
            data = response.json()
            error_msg = data.get('error') or data.get('message') or "Respuesta no encontrada"
            flash(error_msg, "danger")
            return redirect(url_for('respuesta_codigo_bp.listar_respuestas'))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('respuesta_codigo_bp.listar_respuestas'))

# Actualizar una respuesta
@respuesta_codigo_bp.route('/<int:id>/actualizar', methods=['POST'])
def actualizar_respuesta(id):
    url_base_api = current_app.config["URL_BASE_API"]
    headers = {'Clave-De-Autenticacion': current_app.config['TOKEN']}
    api_url = f'{url_base_api}/respuestas/{id}'

    archivo_nombre = request.form.get('archivo_nombre')
    tiempo = request.form.get('tiempo')
    equipo_id = request.form.get('equipo_id')
    desafio_id = request.form.get('desafio_id')

    if not archivo_nombre or not tiempo or not equipo_id or not desafio_id:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('respuesta_codigo_bp.actualizar_respuesta', id=id))

    respuesta_data = {
        'archivo_nombre': archivo_nombre,
        'tiempo': tiempo,
        'equipo_id': int(equipo_id),
        'desafio_id': int(desafio_id)
    }

    try:
        response = requests.put(api_url, json=respuesta_data, headers=headers)
        data = response.json()
        if response.status_code == 200:
            flash(data.get('message', "Respuesta actualizada correctamente"), "success")
            return redirect(url_for('respuesta_codigo_bp.listar_respuestas'))
        else:
            error_msg = data.get('error') or data.get('message') or "Error al actualizar la respuesta"
            flash(error_msg, "danger")
            return redirect(url_for('respuesta_codigo_bp.obtener_respuesta', id=id))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('respuesta_codigo_bp.obtener_respuesta', id=id))