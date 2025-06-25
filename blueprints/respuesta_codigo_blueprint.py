from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import requests

# Crear Blueprint
respuesta_codigo_bp = Blueprint('respuesta_codigo', __name__)

api_url = 'http://localhost:4000/api/respuestas'

UPLOAD_FOLDER = './archivos_codigos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Asignar una nueva respuesta
@respuesta_codigo_bp.route('/crear', methods=['GET','POST'])
def crear_respuesta():
    if request.method == 'POST':
        archivo_nombre = request.files.get('archivo_nombre')
        tiempo = request.form.get('tiempo')
        equipo_id = int(request.form.get('equipo_id'))
        desafio_id = int(request.form.get('desafio_id'))

        if not archivo_nombre or not tiempo or equipo_id is None or desafio_id is None:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('respuesta_codigo.crear_respuesta'))

        try:
            # Intentamos convertir el tiempo al formato correcto
            tiempo = datetime.strptime(tiempo, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            flash('Formato de tiempo incorrecto. Use YYYY-MM-DD HH:MM:SS', 'danger')
            return redirect(url_for('respuesta_codigo.crear_respuesta'))
        
        archivo_url = None
        if archivo_nombre:
            # Guardar el archivo en el servidor
            filename = secure_filename(archivo_nombre.filename) 
            archivo_nombre.save(os.path.join(UPLOAD_FOLDER, filename)) 

            archivo_url = filename 
        else:
            flash('Archivo no permitido', 'danger')
            return redirect(url_for('respuesta_codigo.crear_respuesta_form'))
        respuesta_data = {
            'archivo_nombre': archivo_url,
            'tiempo': tiempo,
            'equipo_id': equipo_id,
            'desafio_id': desafio_id
        }

        try:
            response = requests.post(api_url, json=respuesta_data)

            if response.status_code == 201:
                flash('Respuesta creada correctamente', 'success')
                return redirect(url_for('respuesta_codigo.listar_respuestas'))
            else:
                flash(f'Error: {response.json().get("error")}', 'danger')
                return redirect(url_for('respuesta_codigo.crear_respuesta'))

        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('respuesta_codigo.crear_respuesta'))

    return render_template('crear_respuesta_codigo.html')

# Ruta para obtener todas las respuestas
@respuesta_codigo_bp.route('/')
def listar_respuestas():
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            respuestas = response.json()
            return render_template('listar_respuestas_codigo.html', respuestas=respuestas)
        else:
            flash("Error al obtener las respuestas", "danger")
            return render_template('listar_respuestas_codigo.html', respuestas=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_respuestas_codigo.html', respuestas=[])
    
# Ruta para obtener una respuesta por ID
@respuesta_codigo_bp.route('/<int:id>')
def obtener_respuesta(id):
    try:
        response = requests.get(f'{api_url}/{id}')

        if response.status_code == 200:
            respuesta = response.json()
            return render_template('actualizar_respuesta_codigo.html', respuesta=respuesta)
        else:
            flash("Respuesta no encontrada", "danger")
            return redirect(url_for('respuesta_codigo.listar_respuestas'))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('respuesta_codigo.listar_respuestas'))
    
# Ruta para actualizar una respuesta
@respuesta_codigo_bp.route('/<int:id>/actualizar', methods=['POST'])
def actualizar_respuesta(id):
    archivo_nombre = request.form.get('archivo_nombre')
    tiempo = request.form.get('tiempo')
    equipo_id = request.form.get('equipo_id')
    desafio_id = request.form.get('desafio_id')

    if not archivo_nombre or not tiempo or equipo_id is None or desafio_id is None:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('respuesta_codigo.actualizar_respuesta', id=id))

    respuesta_data = {
        'archivo_nombre': archivo_nombre,
        'tiempo': tiempo,
        'equipo_id': equipo_id,
        'desafio_id': desafio_id
    }

    try:
        response = requests.put(f'{api_url}/{id}', json=respuesta_data)

        if response.status_code == 200:
            flash("Respuesta actualizada con éxito", "success")
            return redirect(url_for('respuesta_codigo.listar_respuestas'))
        else:
            flash("Error al actualizar la respuesta", "danger")
            return redirect(url_for('respuesta_codigo.obtener_respuesta', id=id))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('respuesta_codigo.obtener_respuesta', id=id))