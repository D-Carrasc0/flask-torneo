from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests

# Crear el Blueprint
desafio_bp = Blueprint('desafio', __name__)

# Asignar un desafío
@desafio_bp.route('/crear', methods=['POST'])
def crear_desafio():
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    fase_id = int(request.form.get('fase_id'))
    torneo_id = int(request.form.get('torneo_id'))

    if not titulo or not descripcion or not fase_id or not torneo_id:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('desafio.crear_desafio_form'))

    desafio_data = {
        'titulo': titulo,
        'descripcion': descripcion,
        'fase_id': fase_id,
        'torneo_id': torneo_id
    }

    try:
        api_url = 'http://localhost:4000/api/desafios' 
        response = requests.post(api_url, json=desafio_data)

        if response.status_code == 201:
            flash('Desafío creado correctamente', 'success')
            return redirect(url_for('desafio.listar_desafios'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('desafio.crear_desafio_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('desafio.crear_desafio_form'))

@desafio_bp.route('/crear/form', methods=['GET'])
def crear_desafio_form():
    return render_template('crear_desafio.html')

# Ruta para listar todos los desafíos
@desafio_bp.route('/', methods=['GET'])
def listar_desafios():
    try:
        api_url = 'http://localhost:4000/api/desafios' 
        response = requests.get(api_url)

        if response.status_code == 200:
            desafios = response.json()  # Obtenemos los resultados
            return render_template('listar_desafios.html', desafios=desafios)
        else:
            flash("Error al obtener los desafíos", "danger")
            return render_template('listar_desafios.html', desafios=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_desafios.html', desafios=[])