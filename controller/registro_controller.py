from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests

# Crear Blueprint
registro_bp = Blueprint('registro', __name__)

# Asignar un nuevo registro
@registro_bp.route('/crear', methods=['POST'])
def crear_registro():
    torneo_id = int(request.form.get('torneo_id'))
    equipo_id = int(request.form.get('equipo_id'))

    if not torneo_id or not equipo_id:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('registro.crear_registro_form'))

    registro_data = {
        'torneo_id': torneo_id,
        'equipo_id': equipo_id
    }

    try:
        api_url = 'http://localhost:4000/api/registros'  
        response = requests.post(api_url, json=registro_data)

        if response.status_code == 201:
            flash('Registro creado correctamente', 'success')
            return redirect(url_for('registro.listar_registros'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('registro.crear_registro_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('registro.crear_registro_form'))

@registro_bp.route('/crear/form', methods=['GET'])
def crear_registro_form():
    return render_template('crear_registro_torneo.html')
