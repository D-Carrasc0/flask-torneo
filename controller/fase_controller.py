from flask import Blueprint, request, render_template, flash, redirect, url_for
import requests

# Crear el Blueprint
fase_bp = Blueprint('fase', __name__)

# Asignar una fase
@fase_bp.route('/crear', methods=['POST'])
def crear_fase():
    dificultad = request.form.get('dificultad')
    torneo_id = request.form.get('torneo_id')

    if not dificultad or not torneo_id:
        flash('Faltan datos obligatorios', 'danger')
        return redirect(url_for('fase.crear_fase_form'))

    fase_data = {
        'dificultad': dificultad,
        'torneo_id': torneo_id
    }

    try:
        api_url = 'http://localhost:4000/api/fases'  
        response = requests.post(api_url, json=fase_data)

        if response.status_code == 201:
            flash('Fase creada correctamente', 'success')
            return redirect(url_for('fase.lista_fases'))
        else:
            flash(f'Error: {response.json().get("error")}', 'danger')
            return redirect(url_for('fase.crear_fase_form'))

    except Exception as e:
        flash(f'Error al conectar con la API: {str(e)}', 'danger')
        return redirect(url_for('fase.crear_fase_form'))

@fase_bp.route('/crear/form', methods=['GET'])
def crear_fase_form():
    return render_template('crear_fase.html')

