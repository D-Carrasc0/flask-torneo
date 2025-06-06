from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'  # Necesario para usar flash messages

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para inscripción de equipos
@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_equipo = request.form.get('nombre_equipo')
        avatar = request.files.get('avatar')  # Avatar puede ser un archivo
        pwd_equipo = request.form.get('pwd_equipo')

        # Validaciones simples (puedes añadir más)
        if not nombre_equipo or not pwd_equipo:
            flash('Todos los campos son obligatorios', 'danger')
            return redirect(url_for('inscripcion'))

        # Lógica para procesar el avatar si se sube (por ejemplo, guardarlo en una carpeta)
        if avatar:
            avatar_filename = avatar.filename  # Aquí puedes agregar más lógica para guardar la imagen
            avatar.save(f'./static/avatars/{avatar_filename}')  # Guarda la imagen en la carpeta 'static/avatars'

        # Aquí puedes insertar el equipo en la base de datos (esto es solo un ejemplo)
        # Equipo.crear(nombre_equipo, avatar_filename, pwd_equipo)  # Llama a tu modelo para guardar el equipo

        flash('Equipo inscrito con éxito', 'success')
        return redirect(url_for('index'))  # Redirige a la página principal o a cualquier otra página

    return render_template('inscripcion.html')

# Ruta de login (por si deseas agregar una funcionalidad de login más adelante)
@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
