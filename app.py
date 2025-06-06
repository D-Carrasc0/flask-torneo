from flask import Flask, render_template
from controller.equipo_controller import equipo_bp

app = Flask(__name__)
app.secret_key = 'secret_key'

# Registrar el blueprint para inscripciones
app.register_blueprint(equipo_bp, url_prefix='/')

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
