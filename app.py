from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscripcion', methods=['GET', 'POST'])
def inscripcion():
    if request.method == 'POST':
        nombre_equipo = request.form['nombre_equipo']
        pwd_equipo = request.form['password_equipo']
        integrantes = [
            request.form['integrante1'],
            request.form['integrante2'],
            request.form['integrante3']
        ]

        # Verificar que sean correos distintos
        if len(integrantes) != len(set(integrantes)):
            # talvez enviar un mensaje a traves de flash?
            print()
            return
        
        # Validar que no haya nombres de equipo repetidos
        # Validar correos  (que tengan el formato y que existan en inacap)
        # Validar que un integrante no este ya registrado
        # Guardar integrantes en base de datos
        # Guardar equipo en la base de datos
        
    else:
        return render_template('inscripcion.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True) 