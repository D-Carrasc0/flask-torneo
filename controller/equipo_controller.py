import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

# Crear Blueprint
equipo_bp = Blueprint('equipo', __name__)

# Carpeta donde se guardan temporalmente los avatares
UPLOAD_FOLDER = './static/avatars'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ruta para mostrar formulario y enviar inscripción a la API
@equipo_bp.route('/inscribir', methods=['GET', 'POST'])
def inscribir_equipo():
    if request.method == 'POST':
        nombre_equipo = request.form.get('nombreEquipo')
        pwd_equipo = request.form.get('pwd_equipo')
        avatar = request.files.get('avatar')

        if not nombre_equipo or not pwd_equipo:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('equipo.inscribir_equipo'))

        # Guardar avatar en /static/avatars/
        avatar_url = None
        if avatar:
            filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(UPLOAD_FOLDER, filename)
            avatar.save(avatar_path)
            avatar_url = f'avatars/{filename}'

        # Datos que se enviarán a la API
        equipo_data = {
            'nombre_equipo': nombre_equipo,
            'pwd': pwd_equipo,
            'avatar': avatar_url
        }

        # Enviar datos a la API Node.js
        try:
            api_url = 'http://localhost:4000/api/equipos'
            response = requests.post(api_url, json=equipo_data)

            if response.status_code == 201:
                flash("Equipo inscrito con éxito", "success")
                return redirect(url_for('equipo.lista_equipos'))
            else:
                flash("Error al inscribir el equipo en la API", "danger")
        except Exception as e:
            flash(f"Error al conectar con la API: {str(e)}", "danger")

        return redirect(url_for('equipo.inscribir_equipo'))

    return  render_template('inscribir_equipo.html')


# Ruta para mostrar todos los equipos consultados desde la API

