from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import requests

# Crear Blueprint
respuesta_codigo_bp = Blueprint('respuesta_codigo', __name__)

UPLOAD_FOLDER = './archivos_codigos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Asignar una nueva respuesta
@respuesta_codigo_bp.route('/crear', methods=['POST'])
def crear_respuesta():
    archivo_nombre = request.files.get('archivo_nombre')
    tiempo = request.form.get('tiempo')
    equipo_id = int(request.form.get('equipo_id'))
    desafio_id = int(request.form.get('desafio_id'))

    if not archivo_nombre or not tiempo or equipo_id is None or desafio_id is None:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('respuesta_codigo.crear_respuesta_form'))

    try:
        # Intentamos convertir el tiempo al formato correcto
        tiempo = datetime.strptime(tiempo, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        flash('Formato de tiempo incorrecto. Use YYYY-MM-DD HH:MM:SS', 'danger')
        return redirect(url_for('respuesta_codigo.crear_respuesta_form'))
    
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
        api_url = 'http://localhost:4000/api/respuestas' 
        response = requests.post(api_url, json=respuesta_data)

        if response.status_code == 201:
            flash('Respuesta creada correctamente', 'success')
            return redirect(url_for('respuesta_codigo.listar_respuestas'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('respuesta_codigo.crear_respuesta_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('respuesta_codigo.crear_respuesta_form'))

@respuesta_codigo_bp.route('/crear/form', methods=['GET'])
def crear_respuesta_form():
    return render_template('crear_respuesta_codigo.html')
