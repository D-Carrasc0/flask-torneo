from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import requests

# Crear Blueprint
resultado_fase_bp = Blueprint('resultado_fase', __name__)

# Asignar un nuevo resultado
@resultado_fase_bp.route('/crear', methods=['POST'])
def crear_resultado():
    posicion = int(request.form.get('posicion'))
    puntaje = int(request.form.get('puntaje'))
    media_tiempo = request.form.get('media_tiempo')
    equipo_id = int(request.form.get('equipo_id'))
    fase_id = int(request.form.get('fase_id'))

    if not posicion or puntaje is None or not media_tiempo or equipo_id is None or fase_id is None:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('resultado_fase.crear_resultado_form'))

    try:
        # Intentamos convertir la media_tiempo al formato correcto
        media_tiempo = datetime.strptime(media_tiempo, '%H:%M:%S').time().strftime('%H:%M:%S')
    except ValueError:
        flash('Formato de media_tiempo incorrecto. Use HH:MM:SS', 'danger')
        return redirect(url_for('resultado_fase.crear_resultado_form'))
    
    resultado_data = {
        'posicion': posicion,
        'puntaje': puntaje,
        'media_tiempo': media_tiempo,
        'equipo_id': equipo_id,
        'fase_id': fase_id
    }

    try:
        api_url = 'http://localhost:4000/api/resultados_fase'
        response = requests.post(api_url, json=resultado_data)

        if response.status_code == 201:
            flash('Resultado creado correctamente', 'success')
            return redirect(url_for('resultado_fase.listar_resultados'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('resultado_fase.crear_resultado_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('resultado_fase.crear_resultado_form'))

# Ruta para el formulario de creación de resultado
@resultado_fase_bp.route('/crear/form', methods=['GET'])
def crear_resultado_form():
    return render_template('crear_resultado_fase.html')

# Ruta para obtener todos los resultados
@resultado_fase_bp.route('/')
def listar_resultados():
    try:
        api_url = 'http://localhost:4000/api/resultados_fase'
        response = requests.get(api_url)

        if response.status_code == 200:
            resultados = response.json()
            return render_template('listar_resultados_fase.html', resultados=resultados)
        else:
            flash("Error al obtener los resultados", "danger")
            return render_template('listar_resultados_fase.html', resultados=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_resultados_fase.html', resultados=[])