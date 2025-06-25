from flask import Blueprint, render_template, request, flash, redirect, url_for
import requests

# Crear el Blueprint
desafio_bp = Blueprint('desafio', __name__)

api_url = 'http://localhost:4000/api/desafios'

# Asignar un desafío
@desafio_bp.route('/crear', methods=['GET', 'POST'])
def crear_desafio():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        fase_id = int(request.form.get('fase_id'))
        torneo_id = int(request.form.get('torneo_id'))

        if not titulo or not descripcion or not fase_id or not torneo_id:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('desafio.crear_desafio'))

        desafio_data = {
            'titulo': titulo,
            'descripcion': descripcion,
            'fase_id': fase_id,
            'torneo_id': torneo_id
        }

        try:
            response = requests.post(api_url, json=desafio_data)

            if response.status_code == 201:
                flash('Desafío creado correctamente', 'success')
                return redirect(url_for('desafio.listar_desafios'))
            else:
                flash(f'Error: {response.json().get("error")}', 'danger')
                return redirect(url_for('desafio.crear_desafio'))

        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('desafio.crear_desafio'))

    return render_template('crear_desafio.html')

# Ruta para listar todos los desafíos
@desafio_bp.route('/', methods=['GET'])
def listar_desafios():
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            desafios = response.json()  # Obtenemos los resultadoss
            return render_template('listar_desafios.html', desafios=desafios)
        else:
            flash("Error al obtener los desafíos", "danger")
            return render_template('listar_desafios.html', desafios=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_desafios.html', desafios=[])
    

# Ruta para obtener un desafío por ID
@desafio_bp.route('/<int:id>', methods=['GET'])
def obtener_desafio(id):
    try:
        response = requests.get(f'{api_url}/{id}')

        if response.status_code == 200:
            desafio = response.json()
            return render_template('actualizar_desafio.html', desafio=desafio)
        else:
            flash("Desafío no encontrado", "danger")
            return redirect(url_for('desafio.listar_desafios'))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('desafio.listar_desafios'))
    
# Ruta para actualizar un desafío por ID
@desafio_bp.route('/<int:id>/actualizar', methods=['POST'])
def actualizar_desafio(id):
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        fase_id = request.form.get('fase_id')
        torneo_id = request.form.get('torneo_id')

        if not titulo or not descripcion or not fase_id or not torneo_id:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('desafio.actualizar_desafio', id=id))

        # Datos a enviar para actualizar el desafío
        desafio_data = {
            'titulo': titulo,
            'descripcion': descripcion,
            'fase_id': fase_id,
            'torneo_id': torneo_id
        }

        try:
            response = requests.put(f'{api_url}/{id}', json=desafio_data)

            if response.status_code == 200:
                flash("Desafío actualizado con éxito", "success")
                return redirect(url_for('desafio.listar_desafios'))
            else:
                flash("Error al actualizar el desafío", "danger")
                return redirect(url_for('desafio.obtener_desafio', id=id))
        except Exception as e:
            flash(f"Error al conectar con la API: {str(e)}", "danger")
            return redirect(url_for('desafio.obtener_desafio', id=id))