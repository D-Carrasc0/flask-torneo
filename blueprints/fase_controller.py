from flask import Blueprint, request, render_template, flash, redirect, url_for
import requests

# Crear el Blueprint
fase_bp = Blueprint('fase', __name__)

api_url = 'http://localhost:4000/api/fases'

# Asignar una fase
@fase_bp.route('/crear', methods=['GET','POST'])
def crear_fase():
    if request.method == 'POST':
        dificultad = request.form.get('dificultad')
        torneo_id = int(request.form.get('torneo_id'))
    
        if not dificultad or not torneo_id:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('fase.crear_fase'))

        fase_data = {
            'dificultad': dificultad,
            'torneo_id': torneo_id
        }

        try:
            response = requests.post(api_url, json=fase_data)

            if response.status_code == 201:
                flash('Fase creada correctamente', 'success')
                return redirect(url_for('fase.lista_fases'))
            else:
                flash(f'Error: {response.json().get("error")}', 'danger')
                return redirect(url_for('fase.crear_fase'))

        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('fase.crear_fase'))

    return render_template('crear_fase.html')

# Ruta para listar todas las fases
@fase_bp.route('/', methods=['GET'])
def listar_fases():
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            fases = response.json()  # Obtenemos los resultados
            return render_template('listar_fases.html', fases=fases)
        else:
            flash("Error al obtener las fases", "danger")
            return render_template('listar_fases.html', fases=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_fases.html', fases=[])
    
# Ruta para obtener una fase por ID
@fase_bp.route('/<int:id>', methods=['GET'])
def obtener_fase(id):
    try:
        response = requests.get(f'{api_url}/{id}')

        if response.status_code == 200:
            fase = response.json()
            return render_template('actualizar_fase.html', fase=fase)
        else:
            flash("Error al obtener la fase", "danger")
            return render_template('ver_fase.html', fase=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('ver_fase.html', fase=[])
    
# Ruta para actualizar una fase por ID
@fase_bp.route('/<int:id>', methods=['POST'])
def actualizar_fase(id):
    dificultad = request.json.get('dificultad')
    torneo_id = request.json.get('torneo_id')

    if not dificultad or not torneo_id:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('fase.actualizar_fase', id=id))

    fase_data = {
        'dificultad': dificultad,
        'torneo_id': torneo_id
    }

    try:
        response = requests.put(f'{api_url}/{id}', json=fase_data)

        if response.status_code == 200:
            flash("Fase actualizado con éxito", "success")
            return redirect(url_for('fase.listar_fases'))
        else:
            flash("Error al actualizar la fase", "danger")
            return redirect(url_for('fase.actualizar_fase', id=id))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('fase.actualizar_fase', id=id))