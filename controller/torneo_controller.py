from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

# Crear el Blueprint
torneo_bp = Blueprint('torneo', __name__)

# Asignar un nuevo torneo
@torneo_bp.route('/crear', methods=['POST'])
def crear_torneo():
    nombre = request.form.get('nombre')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_termino = request.form.get('fecha_termino')
    estado = request.form.get('estado')

    if not nombre or not fecha_inicio or not fecha_termino or not estado:
        flash('Faltan datos obligatorios', 'danger')
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
