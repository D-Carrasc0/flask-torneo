from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

# Crear Blueprint
resultado_torneo_bp = Blueprint('resultado_torneo', __name__)

api_url = 'http://localhost:4000/api/resultados_torneo'

# Asignar un nuevo resultado
@resultado_torneo_bp.route('/crear', methods=['GET', 'POST'])
def crear_resultado():
    if request.method == 'POST':
        posicion = int(request.form.get('posicion'))
        puntaje = int(request.form.get('puntaje'))
        media_tiempo = request.form.get('media_tiempo')
        equipo_id = int(request.form.get('equipo_id'))
        torneo_id = int(request.form.get('torneo_id'))

        if not posicion or puntaje is None or not media_tiempo or equipo_id is None or torneo_id is None:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('resultado_torneo.crear_resultado'))

        resultado_data = {
            'posicion': posicion,
            'puntaje': puntaje,
            'media_tiempo': media_tiempo,
            'equipo_id': equipo_id,
            'torneo_id': torneo_id
        }

        try: 
            response = requests.post(api_url, json=resultado_data)

            if response.status_code == 201:
                flash('Resultado creado correctamente', 'success')
                return redirect(url_for('resultado_torneo.listar_resultados'))
            else:
                flash(f'Error: {response.json().get("error")}', 'danger')
                return redirect(url_for('resultado_torneo.crear_resultado'))

        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('resultado_torneo.crear_resultado'))

    return render_template('crear_resultado_torneo.html')

# Ruta para obtener todos los resultados
@resultado_torneo_bp.route('/')
def listar_resultados():
    try:
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
    
# Ruta para obtener un resultado por ID
@resultado_torneo_bp.route('/<int:id>')
def obtener_resultado(id):
    try:
        response = requests.get(f'{api_url}/{id}')

        if response.status_code == 200:
            resultado = response.json()
            return render_template('actualizar_resultado_torneo.html', resultado=resultado)
        else:
            flash("Resultado no encontrado", "danger")
            return redirect(url_for('resultado_torneo.listar_resultados'))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('resultado_torneo.listar_resultados'))

# Ruta para actualizar un resultado
@resultado_torneo_bp.route('/<int:id>/actualizar', methods=['POST'])
def actualizar_resultado(id):
        posicion = request.form.get('posicion')
        puntaje = request.form.get('puntaje')
        media_tiempo = request.form.get('media_tiempo')
        equipo_id = request.form.get('equipo_id')
        torneo_id = request.form.get('torneo_id')

        if not posicion or puntaje is None or not media_tiempo or equipo_id is None or torneo_id is None:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('resultado_torneo.actualizar_resultado', id=id))

        resultado_data = {
            'posicion': posicion,
            'puntaje': puntaje,
            'media_tiempo': media_tiempo,
            'equipo_id': equipo_id,
            'torneo_id': torneo_id
        }

        try:
            response = requests.put(f'{api_url}/{id}', json=resultado_data)

            if response.status_code == 200:
                flash("Resultado actualizado con éxito", "success")
                return redirect(url_for('resultado_torneo.listar_resultados'))
            else:
                flash("Error al actualizar el resultado", "danger")
                return redirect(url_for('resultado_torneo.obtener_resultado', id=id))
        except Exception as e:
            flash(f"Error al conectar con la API: {str(e)}", "danger")
            return redirect(url_for('resultado_torneo.obtener_resultado', id=id))