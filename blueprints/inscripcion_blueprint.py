from flask import render_template, request, jsonify, Blueprint, flash, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import os

inscripcion_bp = Blueprint('inscripcion', __name__)

# Carpeta donde se guardan temporalmente los avatares
UPLOAD_FOLDER = './static/avatars'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

base_api_url = 'http://localhost:4000/api'

@inscripcion_bp.route('/')
def index():
    return render_template('inscripcion.html')

@inscripcion_bp.route('/buscar_usuario')
def buscar_usuario():
    term = request.args.get('term', '')
    try:
        response = requests.get(f'{base_api_url}/integrantes/sugerencias-correo', params={'term': term})
        resultados = response.json()
    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        resultados = []

    return jsonify(resultados)

@inscripcion_bp.route('/inscripcion', methods=['POST'])
def inscribir_equipo():
    nombre_equipo = request.form.get('nombreEquipo')
    pwd_equipo = request.form.get('pwd_equipo')
    avatar = request.files.get('avatar')
    print(nombre_equipo)
    print(pwd_equipo)
    if not nombre_equipo or not pwd_equipo:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('inscripcion.index'))  # Redirigir al formulario

    # Guardar avatar en /static/avatars/
    avatar_url = "SinAvatar"
    if avatar:
        filename = secure_filename(avatar.filename)
        avatar_path = os.path.join(UPLOAD_FOLDER, filename)
        avatar.save(avatar_path)
        avatar_url = f'avatars/{filename}'

    # Validar los integrantes
    integrantes = request.form.getlist("correos[]")
    if len(integrantes) != 3:
        flash("Debe haber exactamente 3 integrantes en el equipo", "danger")
        return redirect(url_for('inscripcion.index'))  # Redirigir al formulario

    # Validar correos institucionales
    for correo in integrantes:
        if not correo.endswith('@inacapmail.cl'):
            flash(f'El correo {correo} no es institucional. Solo se pueden asignar correos institucionales (@inacapmail.cl)', 'danger')
            return redirect(url_for('inscripcion.index'))

    # Datos que se enviarán a la API para crear el equipo
    equipo_data = {
        'nombre_equipo': nombre_equipo,
        'pwd': pwd_equipo,
        'avatar': avatar_url
    }

    
    try:
        # Crear el equipo en la API de Node.js
        api_url = f'{base_api_url}/equipos'
        response = requests.post(api_url, json=equipo_data)

        if response.status_code == 201:
            equipo_id = response.json().get('id_equipo')

            # Asignar integrantes al equipo
            for correo in integrantes:
                rol_id = 2  # Asumimos que el rol por defecto es "Integrante"
                if correo == integrantes[0]:  # El primer integrante es el capitán
                    rol_id = 1
                asignar_data = {
                    'correo': correo,
                    'equipo_id': equipo_id,
                    'rol_id': rol_id
                }

                api_url_integrante = f'{base_api_url}/integrantes/asignar-equipo'
                response_integrante = requests.post(api_url_integrante, json=asignar_data)

                if response_integrante.status_code != 200:
                    flash(f'Error al asignar el integrante con correo {correo}: {response_integrante.json().get("error")}', 'danger')
                    return redirect(url_for('inscripcion.index'))

            flash("Equipo inscrito y miembros asignados correctamente", "success")
            return redirect(url_for('inscripcion.index'))  # Redirigir al índice

        else:
            print("error")
            flash("Error al inscribir el equipo en la API", "danger")
            return redirect(url_for('inscripcion.index'))

    except Exception as e:
        print("eeorr api")
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('inscripcion.index')) 