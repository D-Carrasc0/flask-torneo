import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename  # Para manejar la seguridad de los nombres de los archivos
import os  # Para manejar rutas de archivos
from models.equipo import Equipo  # Importamos el modelo Equipo si necesitas interactuar con tu base de datos local

equipo_bp = Blueprint('equipo', __name__)

# Ruta para crear un nuevo equipo
@equipo_bp.route('/inscribir', methods=['GET', 'POST'])
def inscribir_equipo():
    if request.method == 'POST':
        nombre_equipo = request.form.get('nombreEquipo')
        pwd_equipo = request.form.get('pwd_equipo')
        avatar = request.files.get('avatar')  # Aquí iría la lógica para guardar el avatar

        # Lógica para manejar el avatar
        avatar_url = None
        if avatar:
            # Aquí aseguramos que el nombre del archivo sea seguro
            filename = secure_filename(avatar.filename)
            avatar_url = f'avatars/{filename}'  # Guardamos la imagen en la carpeta avatars
            avatar.save(os.path.join('./static', avatar_url))  # Guardamos el archivo de manera segura

        # Datos del equipo a enviar a la API
        equipo_data = {
            'nombreEquipo': nombre_equipo,
            'pwd_equipo': pwd_equipo,
            'avatar': avatar_url  # La URL del avatar que se subió
        }

        # Realizamos la solicitud POST a la API en el puerto 4000
        try:
            api_url = 'http://localhost:4000/api/equipos/crearEquipo'  # La URL de tu API
            response = requests.post(api_url, json=equipo_data)  # Enviamos los datos en formato JSON

            if response.status_code == 201:  # Código de éxito para creación de recursos
                flash("Equipo inscrito con éxito", "success")
                return redirect(url_for('equipo.lista_equipos'))  # Redirigimos a la lista de equipos
            else:
                flash("Error al inscribir el equipo en la API", "danger")
                return redirect(url_for('equipo.inscribir_equipo'))
        except Exception as e:
            flash(f"Error al conectar con la API: {str(e)}", "danger")
            return redirect(url_for('equipo.inscribir_equipo'))

    return render_template('inscribir_equipo.html')

# Ruta para listar todos los equipos
@equipo_bp.route('/')
def lista_equipos():
    equipos = Equipo.obtener_todos()  # Obtenemos todos los equipos desde tu base de datos local
    return render_template('listar_equipos.html', equipos=equipos)

# Ruta para eliminar un equipo
@equipo_bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_equipo(id):
    if Equipo.eliminar_equipo(id):
        flash("Equipo eliminado con éxito", "success")
    else:
        flash("No se pudo eliminar el equipo", "danger")
    return redirect(url_for('equipo.lista_equipos'))
