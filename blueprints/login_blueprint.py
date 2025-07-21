from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, current_app
import requests

login_bp = Blueprint('login', __name__)

@login_bp.route('/')
def formulario_login():
    return render_template('auth/login.html')

# Ruta para hacer login
@login_bp.route('/login', methods=['POST'])
def login():
    datos_login = {
        "nombre_equipo": request.form.get("nombre_equipo"),
        "pwd": request.form.get("pwd_equipo")
    }

    try:
        url_base_api = current_app.config["URL_BASE_API"]
        response = requests.post(f'{url_base_api}/equipos/login', json=datos_login)
        data = response.json()

        if response.status_code == 200:
            equipo = data['equipo']
            
            session['equipo_id'] = equipo['id_equipo']
            session['nombre_equipo'] = equipo['nombre_equipo']
            
            return redirect(url_for('dashboard_equipo_bp.dashboard_equipo'))

        else:
            error_msg = data.get('message', 'Error desconocido')
            return render_template('auth/login.html', error=error_msg)
        
    except Exception as e:
        return render_template('auth/login.html', error=str(e))
    
@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.formulario_login'))

@login_bp.route('/prueba')
def prueba():
    return render_template('dashboard_equipos/temporal_equipos.html')