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
        response = requests.post(f'{url_base_api}/login', json=datos_login)
        data = response.json()

        if response.status_code == 200:
            session['token'] = data['token']
            session['equipo'] = data['equipo']

            return redirect(url_for('login.perfil'))

        else:
            error_msg = data.get('message', 'Error desconocido')
            return render_template('login.html', error=error_msg)
        
    except Exception as e:
        return render_template('login.html', error=str(e))

@login_bp.route('/perfil')
def perfil():
    token = session.get('token')

    if not token:
        return render_template('auth/login.html', error="Debe iniciar sesión primero"), 401

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        url_base_api = current_app.config["URL_BASE_API"]
        response = requests.get(f'{url_base_api}/protected/perfil', headers=headers)
        data = response.json()

        if response.status_code == 200:
            return render_template('dashboard_usuarios.html', equipo=data["equipo"])
        else:
            return render_template('auth/login.html', error=data.get('message', 'Token inválido')), 401

    except Exception as e:
        return render_template('auth/login.html', error=str(e)), 500
    
@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.formulario_login'))

@login_bp.route('/prueba')
def prueba():
    return render_template('dashboard_equipos/temporal_equipos.html')