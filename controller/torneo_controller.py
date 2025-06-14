from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import requests

# Crear el Blueprint
torneo_bp = Blueprint('torneo', __name__)

# Asignar un nuevo torneo
@torneo_bp.route('/crear', methods=['POST'])
def crear_torneo():
    nombre = request.form.get('nombre')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_termino = request.form.get('fecha_termino')
    estado = int(request.form.get('estado'))

    if not nombre or not fecha_inicio or not fecha_termino or not estado:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('torneo.crear_torneo_form'))

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
        fecha_termino = datetime.strptime(fecha_termino, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        flash('Formato de fecha incorrecto. Use DD/MM/YYYY', 'danger')
        return redirect(url_for('torneo.crear_torneo_form'))
    
    torneo_data = {
        'nombre': nombre,
        'fecha_inicio': fecha_inicio,
        'fecha_termino': fecha_termino,
        'estado': estado
    }

    try:
        api_url = 'http://localhost:4000/api/torneos'  
        response = requests.post(api_url, json=torneo_data)

        if response.status_code == 201:
            flash('Torneo creado correctamente', 'success')
            return redirect(url_for('torneo.listar_torneos'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('torneo.crear_torneo_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('torneo.crear_torneo_form'))

@torneo_bp.route('/crear/form', methods=['GET'])
def crear_torneo_form():
    return render_template('crear_torneo.html')

# Ruta para obtener todos los torneos
@torneo_bp.route('/')
def listar_torneos():
    try:
        api_url = 'http://localhost:4000/api/torneos' 
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