from flask import Flask, render_template
from blueprints.equipo_controller import equipo_bp
from blueprints.integrante_controller import integrante_bp 
from blueprints.fase_controller import fase_bp
from blueprints.desafio_controller import desafio_bp
from blueprints.torneo_controller import torneo_bp
from blueprints.registro_controller import registro_bp
from blueprints.resultado_fase_controller import resultado_fase_bp
from blueprints.resultado_torneo_controller import resultado_torneo_bp
from blueprints.respuesta_codigo_controller import respuesta_codigo_bp

app = Flask(__name__)
app.secret_key = 'secret_key'

# Registrar el blueprint para inscripciones
app.register_blueprint(equipo_bp, url_prefix='/equipo')
app.register_blueprint(integrante_bp, url_prefix='/integrante')
app.register_blueprint(fase_bp, url_prefix='/fase')
app.register_blueprint(desafio_bp, url_prefix='/desafio')
app.register_blueprint(torneo_bp, url_prefix='/torneo')
app.register_blueprint(registro_bp, url_prefix='/registro')
app.register_blueprint(resultado_fase_bp, url_prefix='/resultado_fase') 
app.register_blueprint(resultado_torneo_bp, url_prefix='/resultado_torneo')
app.register_blueprint(respuesta_codigo_bp, url_prefix='/respuesta_codigo')

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de login
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
