from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

# Crear Blueprint
resultado_torneo_bp = Blueprint('resultado_torneo', __name__)

# Asignar un nuevo resultado
@resultado_torneo_bp.route('/crear', methods=['POST'])
def crear_resultado():
    posicion = int(request.form.get('posicion'))
    puntaje = int(request.form.get('puntaje'))
    media_tiempo = request.form.get('media_tiempo')
    equipo_id = int(request.form.get('equipo_id'))
    torneo_id = int(request.form.get('torneo_id'))

    if not posicion or puntaje is None or not media_tiempo or equipo_id is None or torneo_id is None:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('resultado_torneo.crear_resultado_form'))

    resultado_data = {
        'posicion': posicion,
        'puntaje': puntaje,
        'media_tiempo': media_tiempo,
        'equipo_id': equipo_id,
        'torneo_id': torneo_id
    }

    try:
        api_url = 'http://localhost:4000/api/resultados_torneo' 
        response = requests.post(api_url, json=resultado_data)

        if response.status_code == 201:
            flash('Resultado creado correctamente', 'success')
            return redirect(url_for('resultado_torneo.listar_resultados'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('resultado_torneo.crear_resultado_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('resultado_torneo.crear_resultado_form'))

@resultado_torneo_bp.route('/crear/form', methods=['GET'])
def crear_resultado_form():
    return render_template('crear_resultado_torneo.html')

# Ruta para obtener todos los resultados
@resultado_torneo_bp.route('/')
def listar_resultados():
    try:
        api_url = 'http://localhost:4000/api/resultados_torneo' 
        response = requests.get(api_url)

        if response.status_code == 200:
            resultados = response.json()
            return render_template('listar_resultados_torneo.html', resultados=resultados)
        else:
            flash("Error al obtener los resultados", "danger")
            return render_template('listar_resultados_torneo.html', resultados=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_resultados_torneo.html', resultados=[])