from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

# Crear Blueprint
registro_bp = Blueprint('registro', __name__)

api_url = 'http://localhost:4000/api/registros' 

# Asignar un nuevo registro
@registro_bp.route('/crear', methods=['GET','POST'])
def crear_registro():
    if request.method == 'POST':
        torneo_id = int(request.form.get('torneo_id'))
        equipo_id = int(request.form.get('equipo_id'))

        if not torneo_id or not equipo_id:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('registro.crear_registro'))

        registro_data = {
            'torneo_id': torneo_id,
            'equipo_id': equipo_id
        }

        try:
            response = requests.post(api_url, json=registro_data)

            if response.status_code == 201:
                flash('Registro creado correctamente', 'success')
                return redirect(url_for('registro.listar_registros'))
            else:
                flash(f'Error: {response.json().get("error")}', 'danger')
                return redirect(url_for('registro.crear_registro'))

        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('registro.crear_registro'))

    return render_template('crear_registro_torneo.html')

# Ruta para obtener todos los registros
@registro_bp.route('/')
def listar_registros():
    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            registros = response.json()
            return render_template('listar_registros.html', registros=registros)
        else:
            flash("Error al obtener los registros", "danger")
            return render_template('listar_registros.html', registros=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_registros.html', registros=[])
    
# Ruta para obtener un registro por ID
@registro_bp.route('/<int:id>')
def obtener_registro(id):
    try:
        response = requests.get(f'{api_url}/{id}')
        registro = response.json()
        print(registro)
        if response.status_code == 200:
            registro = response.json()
            return render_template('actualizar_registro.html', registro=registro)
        else:
            flash("Registro no encontrado", "danger")
            return redirect(url_for('registro.listar_registros'))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('registro.listar_registros'))
    
# Ruta para actualizar un registro
@registro_bp.route('/<int:id>/actualizar', methods=['POST'])
def actualizar_registro(id):
    if request.method == 'POST':
        torneo_id = request.form.get('torneo_id')
        equipo_id = request.form.get('equipo_id')

        if not torneo_id or not equipo_id:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('registro.actualizar_registro', id=id))

        registro_data = {
            'torneo_id': torneo_id,
            'equipo_id': equipo_id
        }

        try:
            response = requests.put(f'{api_url}/{id}', json=registro_data)

            if response.status_code == 200:
                flash("Registro actualizado con éxito", "success")
                return redirect(url_for('registro.listar_registros'))
            else:
                flash("Error al actualizar el registro", "danger")
                return redirect(url_for('registro.obtener_registro', id=id))
        except Exception as e:
            flash(f"Error al conectar con la API: {str(e)}", "danger")
            return redirect(url_for('registro.obtener_registro', id=id))