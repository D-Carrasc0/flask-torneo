from flask import Blueprint, render_template, session, redirect, url_for, flash, current_app
import requests

dashboard_equipo_bp = Blueprint('dashboard_equipo_bp', __name__)

@dashboard_equipo_bp.route('/dashboard/equipo')
def dashboard_equipo():
    equipo_id = session.get('equipo_id')
    if not equipo_id:
        flash("Debes iniciar sesión primero.", "warning")
        return redirect(url_for('login.formulario_login'))

    clave = current_app.config['TOKEN']
    headers = {'Clave-De-Autenticacion': clave}
    url_base_api = current_app.config["URL_BASE_API"]

    # Equipos
    equipos = requests.get(f"{url_base_api}/equipos", headers=headers).json()

    try:
        equipo_id_int = int(equipo_id)
    except Exception:
        equipo_id_int = -1

    equipo = next((e for e in equipos if int(e.get('CodigoEquipo', -1)) == equipo_id_int), {})

    # Integrantes
    integrantes = requests.get(f"{url_base_api}/integrantes/listar-integrantes", headers=headers).json()
    integrantes_equipo = [i for i in integrantes if i.get('nombre_equipo') == equipo.get('NombreEquipo')]

    # Registros del torneo
    registros = requests.get(f"{url_base_api}/registros", headers=headers).json()
    torneos_ids = [r['torneo_id'] for r in registros if int(r.get('equipo_id', -1)) == equipo_id_int]
    torneos = []
    for torneo_id in torneos_ids:
        torneo = requests.get(f"{url_base_api}/torneos/{torneo_id}", headers=headers).json()
        torneos.append(torneo)

    # Desafíos
    desafios = []
    for torneo_id in torneos_ids:
        ds = requests.get(f"{url_base_api}/desafios", headers=headers).json()
        desafios.extend([d for d in ds if d['torneo_id'] == torneo_id])

    # Resultados
    resultados_torneo = requests.get(f"{url_base_api}/resultados_torneo", headers=headers).json()
    resultados_equipo = [r for r in resultados_torneo if int(r.get('equipo_id', -1)) == equipo_id_int]

    equipo_data = {
        "nombre_equipo": equipo.get("NombreEquipo"),
        "avatar": equipo.get("LogoEquipo"),
        "integrantes": integrantes_equipo,
        "torneos": torneos,
        "desafios": desafios,
        "resultados": resultados_equipo
    }

    return render_template('dashboard_equipos/dashboard_equipo.html', equipo=equipo_data)