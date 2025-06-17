from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import requests

# Crear el Blueprint
torneo_bp = Blueprint('torneo', __name__)

api_url = 'http://localhost:4000/api/torneos'

# Asignar un nuevo torneo
@torneo_bp.route('/crear', methods=['GET','POST'])
def crear_torneo():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_termino = request.form.get('fecha_termino')
        estado = int(request.form.get('estado'))

        if not nombre or not fecha_inicio or not fecha_termino or not estado:
            flash('Faltan datos obligatorios', 'danger')
            return redirect(url_for('torneo.crear_torneo'))

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
            fecha_termino = datetime.strptime(fecha_termino, '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            flash('Formato de fecha incorrecto. Use DD/MM/YYYY', 'danger')
            return redirect(url_for('torneo.crear_torneo'))
        
        torneo_data = {
            'nombre': nombre,
            'fecha_inicio': fecha_inicio,
            'fecha_termino': fecha_termino,
            'estado': estado
        }

        try:
            response = requests.post(api_url, json=torneo_data)

            if response.status_code == 201:
                flash('Torneo creado correctamente', 'success')
                return redirect(url_for('torneo.listar_torneos'))
            else:
                flash(f'Error: {response.json().get("error")}', 'danger')
                return redirect(url_for('torneo.crear_torneo'))

        except Exception as e:
            flash(f'Error al conectar con la API: {str(e)}', 'danger')
            return redirect(url_for('torneo.crear_torneo'))
        
    return render_template('crear_torneo.html')

# Ruta para obtener todos los torneos
@torneo_bp.route('/')
def listar_torneos():
    try: 
        response = requests.get(api_url)

        if response.status_code == 200:
            torneos = response.json()
            return render_template('listar_torneos.html', torneos=torneos)
        else:
            flash("Error al obtener los torneos", "danger")
            return render_template('listar_torneos.html', torneos=[])
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return render_template('listar_torneos.html', torneos=[])
    
# Ruta para obtener torneo por ID
@torneo_bp.route('/<int:id>')
def obtener_torneo(id):
    try:
        response = requests.get(f'{api_url}/{id}')

        if response.status_code == 200:
            torneo = response.json()
            return render_template('actualizar_torneo.html', torneo=torneo)
        else:
            flash("Torneo no encontrado", "danger")
            return redirect(url_for('torneo.listar_torneos'))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('torneo.listar_torneos'))
    
# Ruta para actualizar torneo
@torneo_bp.route('/<int:id>/actualizar', methods=['POST'])
def actualizar_torneo(id):
    nombre = request.form.get('nombre')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_termino = request.form.get('fecha_termino')
    estado = request.form.get('estado')

    if not nombre or not fecha_inicio or not fecha_termino or not estado:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for('torneo.actualizar_torneo', id=id))

    torneo_data = {
        'nombre': nombre,
        'fecha_inicio': fecha_inicio,
        'fecha_termino': fecha_termino,
        'estado': estado
    }

    try:
        response = requests.put(f'{api_url}/{id}', json=torneo_data)

        if response.status_code == 200:
            flash("Torneo actualizado con éxito", "success")
            return redirect(url_for('torneo.listar_torneos'))
        else:
            flash("Error al actualizar el torneo", "danger")
            return redirect(url_for('torneo.obtener_torneo', id=id))
    except Exception as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('torneo.obtener_torneo', id=id))